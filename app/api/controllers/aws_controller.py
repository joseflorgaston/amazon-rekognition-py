import datetime
import uuid
from PIL import ImageDraw
from flask import jsonify, current_app
from app.core.models.draw_label_data import DrawLabelData
from app.core.models.image_data import ImageData
from app.core.models.s3_image_data import S3ImageData
from app.core.use_cases.detect_label_use_case import DetectLabelsUseCase
from app.core.use_cases.decode_64_image import Decode64ImageUseCase
from app.core.use_cases.insert_image_use_case import InsertImageUseCase
from app.core.use_cases.upload_image_to_s3 import UploadImageToS3UseCase
from app.core.use_cases.draw_label_to_image_use_case import DrawLabelToImageUseCase

class AWSController:
    # Sube la imagen a aws
    @staticmethod
    def upload_image(data, bucket_name):
        if 'base64Image' not in data or 'parkingSpotID' not in data or 'cameraID' not in data:
            return jsonify({"success": False, "error": "Missing required fields"}), 400

        # Decodificar la imagen en base64
        image_data = Decode64ImageUseCase.execute(data['base64Image'])

        # Configurar nombre de archivo único
        bucket_name = current_app.config['BUCKET_NAME']
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = uuid.uuid4().hex
        labeled_file_name = f"{data['parkingSpotID']}_{data['cameraID']}_{timestamp}_{unique_id}_labeled.png"
        original_file_name = f"{data['parkingSpotID']}_{data['cameraID']}_{timestamp}_{unique_id}_original.png"

        # Upload original image to s3
        UploadImageToS3UseCase.execute(
            S3ImageData(image_data=image_data, file_name=original_file_name, bucket_name=bucket_name)
        )

        labels = DetectLabelsUseCase().execute(image_data)
        free_count, occupied_count = 0, 0
        draw = ImageDraw.Draw(image_data)

        for label in labels:
            label_name = label['Name'].lower()
            color = 'green' if label_name == 'free' else 'red' if label_name == 'occupied' else None
            if color:
                free_count += (label_name == 'free')
                occupied_count += (label_name == 'occupied')
                box = label['Geometry']['BoundingBox']
                DrawLabelToImageUseCase.execute(
                    DrawLabelData(
                        image=image_data, draw=draw, color=color, box=box
                    )
                )

        # Upload labeled image to s3
        UploadImageToS3UseCase.execute(
            S3ImageData(image_data=image_data, file_name=labeled_file_name, bucket_name=bucket_name)
        )
        
        # Construir URL de la imagen
        labeled_image_url = f"https://{bucket_name}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/{labeled_file_name}"
        original_image_url = f"https://{bucket_name}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/{original_file_name}"

        InsertImageUseCase.execute(
            image_data= ImageData(
                parking_spot_id= data['parking_spot_id'], 
                camera_id= data['camera_id'], 
                labeled_image_url= labeled_image_url,
                original_image_url= original_image_url,
                free_count=free_count,
                occupied_count=occupied_count,
                date= datetime.now()
            )
        )

        # Responder con el URL de la imagen y los datos recibidos
        return jsonify({
            "success": True,
            "labeled_image_url": labeled_image_url,
            "original_image_url": original_image_url,
            "parkingSpotID": data['parkingSpotID'],
            "cameraID": data['cameraID'],
            "labeled_file_name": labeled_file_name,
            "original_file_name": original_file_name, 
        }), 200
    