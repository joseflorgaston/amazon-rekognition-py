from app.data.repositories.parking_spot_repository.parking_spot_repository import ParkingSpotRepository

class GetParkingSpotsUseCase:
    def __init__(self):
        self.parking_spot_repository = ParkingSpotRepository()

    def execute(self):
        response = self.parking_spot_repository.get_parking_spots()
        return response
