from app.core.exceptions import ModelAlreadyStoppedException
from app.data.repositories.label_repository import ParkingLotRepository

class StopModelUseCase:
    def __init__(self):
        self.label_repository = ParkingLotRepository()

    def execute(self):
        # Comprobar si el modelo ya está detenido
        if not self.label_repository.is_model_running():
            raise ModelAlreadyStoppedException("Model is already stopped")

        # Detener el modelo
        response = self.label_repository.stop_model()
        return response
