from app.core.exceptions import ModelAlreadyRunningException
from app.core.models.s3_image_data import S3ImageData
from app.data.repositories.label_repository import ParkingLotRepository

class UploadImageToS3UseCase:
    def __init__(self):
        self.label_repository = ParkingLotRepository()

    def execute(self, s3_image: S3ImageData):
        response = self.label_repository.upload_image_to_s3(s3_image)
        return response
