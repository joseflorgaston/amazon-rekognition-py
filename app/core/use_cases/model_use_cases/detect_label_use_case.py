from app.data.repositories.model_repository.model_repository import ModelRepository

class DetectLabelsUseCase:
    def __init__(self, model_repository=None):
        self.model_repository = model_repository or ModelRepository()

    def execute(self, image_bytes):
        labels = self.model_repository.detect_labels(image_bytes)
        return labels
