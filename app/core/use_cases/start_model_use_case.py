from app.core.exceptions import ModelAlreadyRunningException
from app.data.repositories.label_repository import ParkingLotRepository

class StartModelUseCase:
    def __init__(self):
        self.label_repository = ParkingLotRepository()

    def execute(self):
        # Comprobar si el modelo ya está en ejecución
        if self.label_repository.is_model_running():
            raise ModelAlreadyRunningException("Model is already running")

        # Iniciar el modelo
        response = self.label_repository.start_model()
        return response
