from app.data.repositories.camera_repository.camera_repository import CameraRepository

class GetCamerasUseCase:
    def __init__(self):
        self.camera_repository = CameraRepository()

    def execute(self):
        response = self.camera_repository.get_cameras()
        return response
