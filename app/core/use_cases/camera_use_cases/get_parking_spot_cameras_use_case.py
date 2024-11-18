from app.data.repositories.camera_repository.camera_repository import CameraRepository

class GetParkingSpotCamerasUseCase:
    def __init__(self):
        self.camera_repository = CameraRepository()

    def execute(self, parking_spot_id: str):
        response = self.camera_repository.get_parking_spot_cameras(parking_spot_id)
        return response
