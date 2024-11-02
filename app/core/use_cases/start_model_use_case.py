from app.data.repositories.label_repository import LabelRepository

class StartModelUseCase:
    def __init__(self, label_repository=None):
        self.label_repository = label_repository or LabelRepository()

    def execute(self):
        return self.label_repository.start_model()
