from bson import ObjectId
from app.core.models.camera_data import CameraData
from app.data.repositories.label_repository import ParkingLotRepository

class InsertCameraUseCase:
    def __init__(self):
        self.label_repository = ParkingLotRepository()

    def execute(self, camera: CameraData):
        if isinstance(camera.parking_spot_id, str):
            camera.parking_spot_id = ObjectId(camera.parking_spot_id)
        
        response = self.label_repository.insert_camera(camera)
        return response
