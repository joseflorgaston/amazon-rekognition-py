from bson import ObjectId
from app.core.models.image_data import ImageData
from app.data.repositories.label_repository import ParkingLotRepository

class InsertImageUseCase:
    def __init__(self):
        self.label_repository = ParkingLotRepository()

    def execute(self, image: ImageData):
        if isinstance(image.parking_spot_id, str):
            image.parking_spot_id = ObjectId(image.parking_spot_id)
        
        if isinstance(image.camera_id, str):
            image.camera_id = ObjectId(image.camera_id)
            
        response = self.label_repository.insert_image(image)
        return response
