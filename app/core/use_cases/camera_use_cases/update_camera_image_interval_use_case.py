from app.data.repositories.camera_repository.camera_repository import CameraRepository

class UpdateCameraImageIntervalUseCase:
    def __init__(self):
        self.camera_repository = CameraRepository()

    def execute(self, camera_id: str, image_interval: int):
        response = self.camera_repository.update_camera_image_interval(camera_id, image_interval)
        return response
