from app.core.models.camera_data import CameraData
from app.data.services.camera_service import CameraService

class CameraRepository:
    def __init__(self, camera_service=None):
        self.camera_service = camera_service or CameraService()

    def insert_camera(self, camera: CameraData):
        return self.camera_service.insert_camera(camera)
    
    def delete_camera(self, camera_id: str):
        return self.camera_service.delete_camera(camera_id)
