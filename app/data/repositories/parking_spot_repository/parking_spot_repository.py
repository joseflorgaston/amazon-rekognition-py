from app.core.models.parking_spot_data import ParkingSpotData
from app.data.services.parking_spot_service import ParkingSpotService

class ParkingSpotRepository:
    def __init__(self):
        self.parking_spot_service = ParkingSpotService()

    def insert_parking_spot(self, parking_spot: ParkingSpotData):
        return self.parking_spot_service.insert_parking_spot(parking_spot)
    
    def delete_parking_spot(self, parking_spot_id: str):
        return self.parking_spot_service.insert_parking_spot(parking_spot_id)
