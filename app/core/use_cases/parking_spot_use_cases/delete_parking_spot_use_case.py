from app.data.repositories.parking_spot_repository.parking_spot_repository import ParkingSpotRepository

class DeleteParkingSpotUseCase:
    def __init__(self):
        self.parking_spot_repository = ParkingSpotRepository()

    def execute(self, parking_spot_id: str):
        response = self.parking_spot_repository.delete_parking_spot(parking_spot_id)
        return response
