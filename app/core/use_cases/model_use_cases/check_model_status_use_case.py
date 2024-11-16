from app.data.repositories.model_repository.model_repository import ModelRepository

class CheckModelStatusUseCase:
    def __init__(self, model_repository=None):
        self.model_repository = model_repository or ModelRepository()

    def execute(self):
        return self.model_repository.is_model_running()
