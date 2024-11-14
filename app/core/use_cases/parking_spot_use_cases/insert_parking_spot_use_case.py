from app.core.models.parking_spot_data import ParkingSpotData
from app.data.repositories.parking_spot_repository.parking_spot_repository import ParkingSpotRepository

class InsertParkingSpotUseCase:
    def __init__(self):
        self.parking_spot_repository = ParkingSpotRepository()

    def execute(self, parking_spot: ParkingSpotData):
        response = self.parking_spot_repository.insert_parking_spot(parking_spot)
        return response
