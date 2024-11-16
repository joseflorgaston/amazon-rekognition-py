from app.core.models.camera_data import CameraData
from app.data.services.camera_service import CameraService

class CameraRepository:
    def __init__(self, camera_service=None):
        self.camera_service = camera_service or CameraService()
        
    def get_cameras(self):
        return self.camera_service.get_cameras()
    
    def get_parking_spot_cameras(self, parking_spot_id: str):
        return self.camera_service.get_parking_spot_cameras(parking_spot_id)

    def insert_camera(self, camera: CameraData):
        return self.camera_service.insert_camera(camera)

    def update_camera(self, camera_id: str, camera: CameraData):
        return self.camera_service.update_camera(camera_id, camera)
    
    def update_camera_max_results(self, camera_id: str, max_results: int):
        return self.camera_service.update_camera_max_results(camera_id, max_results)
    
    def update_camera_image_interval(self, camera_id: str, image_interval: int):
        return self.camera_service.update_camera_image_interval(camera_id, image_interval)
        
    def delete_camera(self, camera_id: str):
        return self.camera_service.delete_camera(camera_id)
