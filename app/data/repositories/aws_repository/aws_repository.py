from app.core.models.s3_image_data import S3ImageData
from app.data.services.aws_service import AWSService

class AwsRepository:
    def __init__(self, aws_service=None):
        self.aws_service = aws_service or AWSService()

    def upload_image_to_s3(self, s3_image_data: S3ImageData):
        return self.aws_service.upload_image_to_s3(s3_image_data)
    