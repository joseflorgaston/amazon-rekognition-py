from app.core.exceptions import ModelAlreadyRunningException
from app.data.repositories.model_repository.model_repository import ModelRepository

class StartModelUseCase:
    def __init__(self):
        self.model_repository = ModelRepository()

    def execute(self):
        # Comprobar si el modelo ya está en ejecución
        if self.model_repository.is_model_running():
            raise ModelAlreadyRunningException("Model is already running")

        # Iniciar el modelo
        response = self.model_repository.start_model()
        return response
