from app.core.models.s3_image_data import S3ImageData
from app.data.repositories.aws_repository.aws_repository import AwsRepository

class UploadImageToS3UseCase:
    def __init__(self):
        self.aws_repository = AwsRepository()

    def execute(self, s3_image: S3ImageData):
        response = self.aws_repository.upload_image_to_s3(s3_image)
        return response
