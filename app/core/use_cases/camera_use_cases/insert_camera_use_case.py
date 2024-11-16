from bson import ObjectId
from app.core.models.parking_spot_data import ParkingSpotData
from app.data.repositories.camera_repository.camera_repository import CameraRepository

class InsertCameraUseCase:
    def __init__(self):
        self.camera_repository = CameraRepository()

    def execute(self, camera: ParkingSpotData):
        response = self.camera_repository.insert_camera(camera)
        return response
