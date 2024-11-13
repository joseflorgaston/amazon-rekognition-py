from app.core.models.parking_spot_data import ParkingSpotData
from app.data.repositories.label_repository import ParkingLotRepository

class InsertParkingSpotUseCase:
    def __init__(self):
        self.label_repository = ParkingLotRepository()

    def execute(self, parking_spot: ParkingSpotData):
        response = self.label_repository.insert_parking_spot(parking_spot)
        return response
