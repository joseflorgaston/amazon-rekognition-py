from app.data.repositories.label_repository import ParkingLotRepository

class DetectLabelsUseCase:
    def __init__(self, label_repository=None):
        self.label_repository = label_repository or ParkingLotRepository()

    def execute(self, image_bytes):
        labels = self.label_repository.detect_labels(image_bytes)
        return labels
