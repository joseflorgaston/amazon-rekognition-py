from flask import jsonify
from app.config.s3_client import get_s3_client
from app.core.models.s3_image_data import S3ImageData
from app.interfaces.aws_interface import AwsInterface

class AWSService(AwsInterface):
    def __init__(self):
        self.s3_client = get_s3_client()

    # Sube una imagen en formato base64 al s3.
    def upload_image_to_s3(self, s3_image_data: S3ImageData):
        try:
            self.s3_client.put_object(
                Bucket=s3_image_data.bucket_name,
                Key=s3_image_data.file_name,
                Body=s3_image_data.image_data,
                ContentType='image/png'
            )
            return jsonify({"success": True, "message": "Image uploaded to S3"})
        except Exception as e:
            print(f"Failed to upload image: {e}")
            return jsonify({"success": False, "message": f"Failed to upload image to S3: {e}"}), 500
