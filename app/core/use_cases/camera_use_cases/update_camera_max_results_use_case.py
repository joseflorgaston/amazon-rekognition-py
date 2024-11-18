from app.data.repositories.camera_repository.camera_repository import CameraRepository

class UpdateCameraMaxResultsUseCase:
    def __init__(self):
        self.camera_repository = CameraRepository()

    def execute(self, camera_id: str, max_results: int):
        response = self.camera_repository.update_camera_max_results(camera_id, max_results)
        return response
