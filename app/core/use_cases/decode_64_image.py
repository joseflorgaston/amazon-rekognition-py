from app.core.exceptions import ModelAlreadyRunningException
from app.data.repositories.label_repository import ParkingLotRepository

class Decode64ImageUseCase:
    def __init__(self):
        self.label_repository = ParkingLotRepository()

    def execute(self, base64_str):
        # Decodificar base64
        response = self.label_repository.decode_base64_image(base64_str)
        return response
