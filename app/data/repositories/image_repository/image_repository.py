from app.core.models.image_data import ImageData
from app.data.services.image_service import ImageService

class ImageRepository:
    def __init__(self, image_service=None):
        self.image_service = image_service or ImageService()

    def insert_image(self, image: ImageData):
        return self.image_service.insert_image(image)

    def delete_image(self, image_id: str):
        return self.image_service.delete_image(image_id)
