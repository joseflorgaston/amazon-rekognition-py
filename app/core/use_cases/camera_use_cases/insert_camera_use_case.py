from bson import ObjectId
from app.core.models.camera_data import CameraData
from app.data.repositories.camera_repository.camera_repository import CameraRepository

class InsertCameraUseCase:
    def __init__(self):
        self.camera_repository = CameraRepository()

    def execute(self, camera: CameraData):
        if isinstance(camera.parking_spot_id, str):
            camera.parking_spot_id = ObjectId(camera.parking_spot_id)
        
        response = self.camera_repository.insert_camera(camera)
        return response
