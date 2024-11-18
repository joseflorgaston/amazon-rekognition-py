from app.core.models.parking_spot_data import ParkingSpotData
from app.data.services.parking_spot_service import ParkingSpotService

class ParkingSpotRepository:
    def __init__(self):
        self.parking_spot_service = ParkingSpotService()

    def get_parking_spots(self):
        return self.parking_spot_service.get_parking_spots()

    def get_parking_spot(self, parking_spot_id: str):
        return self.parking_spot_service.get_parking_spot(parking_spot_id)

    def insert_parking_spot(self, parking_spot: ParkingSpotData):
        return self.parking_spot_service.insert_parking_spot(parking_spot)

    def update_parking_spot(self, parking_spot_id: str, parking_spot: ParkingSpotData):
        return self.parking_spot_service.update_parking_spot(parking_spot_id, parking_spot)

    def delete_parking_spot(self, parking_spot_id: str):
        return self.parking_spot_service.delete_parking_spot(parking_spot_id)
