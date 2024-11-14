from bson import ObjectId
from app.core.models.image_data import ImageData
from app.data.repositories.image_repository.image_repository import ImageRepository

class InsertImageUseCase:
    def __init__(self):
        self.image_repository = ImageRepository()

    def execute(self, image: ImageData):
        if isinstance(image.parking_spot_id, str):
            image.parking_spot_id = ObjectId(image.parking_spot_id)
        
        if isinstance(image.camera_id, str):
            image.camera_id = ObjectId(image.camera_id)
            
        response = self.image_repository.insert_image(image)
        return response
