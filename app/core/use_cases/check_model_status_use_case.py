from app.data.repositories.label_repository import ParkingLotRepository

class CheckModelStatusUseCase:
    def __init__(self, label_repository=None):
        self.label_repository = label_repository or ParkingLotRepository()

    def execute(self):
        # Llama al repositorio para verificar el estado del modelo
        return self.label_repository.is_model_running()
