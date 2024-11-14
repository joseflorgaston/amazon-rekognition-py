from app.core.exceptions import ModelAlreadyStoppedException
from app.data.repositories.model_repository.model_repository import ModelRepository

class StopModelUseCase:
    def __init__(self):
        self.model_repository = ModelRepository()

    def execute(self):
        # Comprobar si el modelo ya está detenido
        if not self.model_repository.is_model_running():
            raise ModelAlreadyStoppedException("Model is already stopped")

        # Detener el modelo
        response = self.model_repository.stop_model()
        return response
