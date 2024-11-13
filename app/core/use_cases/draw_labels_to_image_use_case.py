from app.core.models.draw_labels_data import DrawLabelsData
from app.data.repositories.label_repository import ParkingLotRepository

class DrawLabelsToImageUseCase:
    def __init__(self):
        self.label_repository = ParkingLotRepository()

    def execute(self, draw_label: DrawLabelsData):
        response = self.label_repository.draw_labels_to_image(draw_label)
        return response
