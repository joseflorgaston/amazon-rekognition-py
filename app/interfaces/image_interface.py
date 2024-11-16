from abc import ABC, abstractmethod

from app.core.models.image_data import ImageData

class ImageInterface(ABC):
    @abstractmethod
    def get_last_image(self, camera_id: str):
        pass
    
    @abstractmethod
    def insert_image(self, image: ImageData):
        pass
    
    @abstractmethod
    def delete_image(self, image_id: str):
        pass
    