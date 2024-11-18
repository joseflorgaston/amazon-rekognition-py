from app.core.models.camera_data import CameraData
from app.data.repositories.camera_repository.camera_repository import CameraRepository

class UpdateCameraUseCase:
    def __init__(self):
        self.camera_repository = CameraRepository()

    def execute(self, camera_id: str, camera: CameraData):
        response = self.camera_repository.update_camera(camera_id, camera)
        return response
