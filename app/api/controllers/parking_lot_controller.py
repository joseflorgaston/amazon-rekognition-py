
from datetime import datetime
import uuid
from flask import current_app, jsonify
from PIL import ImageDraw
from app.core.models.camera_data import CameraData
from app.core.models.draw_label_data import DrawLabelData
from app.core.models.draw_labels_data import DrawLabelsData
from app.core.models.image_data import ImageData
from app.core.models.parking_spot_data import ParkingSpotData
from app.core.models.s3_image_data import S3ImageData
from app.core.use_cases.decode_64_image import Decode64ImageUseCase
from app.core.use_cases.detect_label_use_case import DetectLabelsUseCase
from app.core.use_cases.draw_label_to_image_use_case import DrawLabelToImageUseCase
from app.core.use_cases.draw_labels_to_image_use_case import DrawLabelsToImageUseCase
from app.core.use_cases.upload_image_to_s3 import UploadImageToS3UseCase
from app.core.use_cases.insert_image_use_case import InsertImageUseCase
from app.core.use_cases.insert_camera_use_case import InsertCameraUseCase
from app.core.use_cases.insert_parking_spot_use_case import InsertParkingSpotUseCase

class ParkingLotController:
    @staticmethod
    def insert_parking_spot(data):
        return InsertParkingSpotUseCase().execute(
            parking_spot = ParkingSpotData(
                name=data['name'],
                address=data['address'],
                location= data['location'],
                created_at= datetime.now()
            )
        )

    @staticmethod
    def insert_camera(data):
        return InsertCameraUseCase().execute(
            CameraData(
                parking_spot_id=data['parking_spot_id'],
                image_interval=data["image_interval"],
                created_at=datetime.now(),
                identifier=data['identifier'],
                max_results=data['max_results'],
            )
        )
    
    @staticmethod
    def insert_image(data):
        if 'base64Image' not in data or 'parkingSpotID' not in data or 'cameraID' not in data:
            return jsonify({"success": False, "error": "Missing required fields"}), 400

        # Decodificar la imagen en base64
        image_data = Decode64ImageUseCase().execute(data['base64Image'])

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
        image_labeled = DrawLabelsToImageUseCase().execute(
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
    
    