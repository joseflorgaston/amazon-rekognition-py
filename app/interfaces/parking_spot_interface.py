from abc import ABC, abstractmethod

from app.core.models.parking_spot_data import ParkingSpotData

class ParkingSpotInterface(ABC):
    @abstractmethod
    def get_parking_spots(self):
        pass
    
    @abstractmethod
    def get_parking_spot(self, parking_spot_id: str):
        pass
    
    @abstractmethod
    def insert_parking_spot(self, parking_spot: ParkingSpotData):
        pass
    
    @abstractmethod
    def update_parking_spot(self, parking_spot_id: str, parking_spot: ParkingSpotData):
        pass
    
    @abstractmethod
    def delete_parking_spot(self, parking_spot_id: str):
        pass