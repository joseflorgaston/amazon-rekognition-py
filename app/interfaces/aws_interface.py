from abc import ABC, abstractmethod
from app.core.models.s3_image_data import S3ImageData

class AwsInterface(ABC):
    @abstractmethod
    def upload_image_to_s3(self, s3_image_data: S3ImageData):
        pass
    