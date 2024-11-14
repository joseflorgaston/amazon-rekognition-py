from app.data.repositories.camera_repository.camera_repository import CameraRepository

class DeleteCameraUseCase:
    def __init__(self):
        self.camera_repository = CameraRepository()

    def execute(self, camera_id: str):
        response = self.camera_repository.delete_camera(camera_id)
        return response
