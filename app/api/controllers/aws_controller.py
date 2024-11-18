import datetime
import uuid
from flask import jsonify, current_app
from app.core.helpers.image_helper import ImageHelper
from app.core.models.image_data import ImageData
from app.core.models.s3_image_data import S3ImageData
from app.core.use_cases.image_use_cases.insert_image_use_case import InsertImageUseCase
from app.core.use_cases.image_use_cases.upload_image_to_s3 import UploadImageToS3UseCase

class AWSController:
    # Sube la imagen a aws
    @staticmethod
    def upload_image(data, bucket_name):
        if 'base64Image' not in data:
            return jsonify({"success": False, "error": "Missing required fields"}), 400

        # Decodificar la imagen en base64
        image_data = ImageHelper.decode_base64_image(data['base64Image'])

        # Configurar nombre de archivo único
        bucket_name = current_app.config['BUCKET_NAME']
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = uuid.uuid4().hex
        original_file_name = f"{data['parkingSpotID']}_{data['cameraID']}_{timestamp}_{unique_id}_original.png"

        # Upload original image to s3
        UploadImageToS3UseCase.execute(
            S3ImageData(image_data=image_data, file_name=original_file_name, bucket_name=bucket_name)
        )
        
        # Construir URL de la imagen
        image_url = f"https://{bucket_name}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/{original_file_name}"

        InsertImageUseCase.execute(
            image_data= ImageData(
                parking_spot_id= data['parking_spot_id'], 
                camera_id= data['camera_id'], 
                image_url= image_url,
                date= datetime.now()
            )
        )

        # Responder con el URL de la imagen y los datos recibidos
        return jsonify({
            "success": True,
            "image_url": image_url,
            "parkingSpotID": data['parkingSpotID'],
            "cameraID": data['cameraID'],
            "file_name": original_file_name, 
        }), 200
    