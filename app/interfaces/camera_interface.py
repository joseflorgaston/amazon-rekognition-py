from abc import ABC, abstractmethod

from app.core.models.camera_data import CameraData

class CameraInterface(ABC):
    @abstractmethod
    def get_cameras(self):
        pass
    
    @abstractmethod
    def get_parking_spot_cameras(self, parking_spot_id: str):
        pass
    
    @abstractmethod
    def insert_camera(self, camera: CameraData):
        pass
    
    @abstractmethod
    def update_camera(self, camera_id: str, camera: CameraData):
        pass
    
    @abstractmethod
    def update_camera_max_results(self, camera_id: str, max_results: int):
        pass
    
    @abstractmethod
    def update_camera_image_interval(self, camera_id: str, image_interval: int):
        pass
    
    @abstractmethod
    def delete_camera(self, camera_id: str):
        pass