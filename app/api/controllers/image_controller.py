
from datetime import datetime
from io import BytesIO
from PIL import Image
import uuid
from flask import current_app, jsonify
from app.core.models.draw_labels_data import DrawLabelsData
from app.core.models.image_data import ImageData
from app.core.models.s3_image_data import S3ImageData
from app.core.use_cases.image_use_cases.delete_image_use_case import DeleteImageUseCase
from app.core.use_cases.model_use_cases.detect_label_use_case import DetectLabelsUseCase
from app.core.use_cases.image_use_cases.upload_image_to_s3 import UploadImageToS3UseCase
from app.core.use_cases.image_use_cases.insert_image_use_case import InsertImageUseCase
from app.core.use_cases.image_use_cases.get_last_image_use_case import GetLastImageUseCase
from app.core.helpers.image_helper import ImageHelper

class ImageController:
    @staticmethod
    def get_last_image(camera_id: str):
        return GetLastImageUseCase().execute(camera_id)
    
    @staticmethod
    def insert_image(data):
        if 'image' not in data or 'parking_spot_id' not in data or 'camera_id' not in data or 'max_results' not in data:
            return jsonify({"success": False, "error": "Missing required fields"}), 400
        
        image_data = ImageHelper().decode_base64_image(data['image'])
        
        bucket_name = current_app.config['BUCKET_NAME']
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = uuid.uuid4().hex
        labeled_file_name = f"labeled/{data['parking_spot_id']}_{data['camera_id']}_{timestamp}_{unique_id}.png"
        original_file_name = f"original/{data['parking_spot_id']}_{data['camera_id']}_{timestamp}_{unique_id}.png"

        # Upload original image to s3
        UploadImageToS3UseCase().execute(
            S3ImageData(
                image_data = image_data, 
                file_name = original_file_name, 
                bucket_name = bucket_name, 
                max_results = data['max_results']
            )
        )

        # labels = DetectLabelsUseCase().execute(image_data)
        
        image_pil = Image.open(BytesIO(image_data))
        image_labeled = ImageHelper().draw_labels_to_image(
            DrawLabelsData(
                image= image_pil,
                # labels= labels
                labels= []
            )
        )

        # Convertir la imagen etiquetada (PIL) a bytes
        image_labeled_bytes = ImageHelper.pil_image_to_bytes(image_labeled.image)

        # Upload labeled image to s3
        UploadImageToS3UseCase().execute(
            S3ImageData(
                image_data= image_labeled_bytes, 
                file_name= labeled_file_name, 
                bucket_name= bucket_name, 
                max_results= data['max_results']
            )
        )
        
        # Construir URL de la imagen
        labeled_image_url = f"https://{bucket_name}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/{labeled_file_name}"
        original_image_url = f"https://{bucket_name}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/{original_file_name}"

        InsertImageUseCase().execute(
            image= ImageData(
                parking_spot_id= data['parking_spot_id'],
                camera_id= data['camera_id'],
                labeled_image_url= labeled_image_url,
                original_image_url= original_image_url,
                free_spaces= image_labeled.free_spaces,
                occupied_spaces= image_labeled.occupied_spaces,
                date= datetime.now()
            )
        )
        
        print('Image inserted to database')

        # Responder con el URL de la imagen y los datos recibidos
        return jsonify({
            "success": True,
            "labeled_image_url": labeled_image_url,
            "original_image_url": original_image_url,
            "parking_spot_id": data['parking_spot_id'],
            "camera_id": data['camera_id'],
            "labeled_file_name": labeled_file_name,
            "original_file_name": original_file_name,
            "message": "Image inserted successfully",
        }), 200

    @staticmethod
    def delete_image(image_id: str):
        return DeleteImageUseCase().execute(image_id)
