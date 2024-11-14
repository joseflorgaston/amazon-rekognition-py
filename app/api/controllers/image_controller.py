
from datetime import datetime
import uuid
from flask import current_app, jsonify
from app.core.models.draw_labels_data import DrawLabelsData
from app.core.models.image_data import ImageData
from app.core.models.s3_image_data import S3ImageData
from app.core.use_cases.image_use_cases.delete_image_use_case import DeleteImageUseCase
from app.core.use_cases.model_use_cases.detect_label_use_case import DetectLabelsUseCase
from app.core.use_cases.image_use_cases.upload_image_to_s3 import UploadImageToS3UseCase
from app.core.use_cases.image_use_cases.insert_image_use_case import InsertImageUseCase
from app.core.helpers.image_helper import ImageHelper

class ImageController:
    @staticmethod
    def insert_image(data):
        if 'base64Image' not in data or 'parkingSpotID' not in data or 'cameraID' not in data:
            return jsonify({"success": False, "error": "Missing required fields"}), 400

        # Decodificar la imagen en base64
        image_data = ImageHelper().decode_base64_image(data['base64Image'])

        # Configurar nombre de archivo único
        bucket_name = current_app.config['BUCKET_NAME']
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = uuid.uuid4().hex
        labeled_file_name = f"{data['parkingSpotID']}_{data['cameraID']}_{timestamp}_{unique_id}_labeled.png"
        original_file_name = f"{data['parkingSpotID']}_{data['cameraID']}_{timestamp}_{unique_id}_original.png"

        # Upload original image to s3
        UploadImageToS3UseCase().execute(
            S3ImageData(image_data=image_data, file_name=original_file_name, bucket_name=bucket_name)
        )

        labels = DetectLabelsUseCase().execute(image_data)
        image_labeled = ImageHelper().draw_labels_to_image(
            draw_label= DrawLabelsData(
                image= image_data,
                labels= labels
            )
        )

        # Upload labeled image to s3
        UploadImageToS3UseCase().execute(
            S3ImageData(image_data=image_labeled.image, file_name=labeled_file_name, bucket_name=bucket_name)
        )
        
        # Construir URL de la imagen
        labeled_image_url = f"https://{bucket_name}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/{labeled_file_name}"
        original_image_url = f"https://{bucket_name}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/{original_file_name}"

        InsertImageUseCase().execute(
            image_data= ImageData(
                parking_spot_id= data['parking_spot_id'],
                camera_id= data['camera_id'],
                labeled_image_url= labeled_image_url,
                original_image_url= original_image_url,
                free_count=image_labeled.free_spaces,
                occupied_count=image_labeled.occupied_spaces,
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
            "message": "Image inserted successfully",
        }), 200

    @staticmethod
    def delete_image(image_id):
        DeleteImageUseCase().execute(image_id)

        return jsonify({
            "success": True,
            "message": "Image deleted successfully",
        }), 200
