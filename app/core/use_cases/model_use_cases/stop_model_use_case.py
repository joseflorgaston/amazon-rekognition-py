from app.core.exceptions import ModelAlreadyStoppedException
from app.data.repositories.model_repository.model_repository import ModelRepository

class StopModelUseCase:
    def __init__(self):
        self.model_repository = ModelRepository()

    def execute(self):
        response = self.model_repository.stop_model()
        return response
