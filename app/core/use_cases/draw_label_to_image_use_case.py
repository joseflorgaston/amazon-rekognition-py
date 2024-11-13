from app.core.exceptions import ModelAlreadyRunningException
from app.core.models.draw_label_data import DrawLabelData
from app.data.repositories.label_repository import ParkingLotRepository

class DrawLabelToImageUseCase:
    def __init__(self):
        self.label_repository = ParkingLotRepository()

    def execute(self, draw_label: DrawLabelData):
        response = self.label_repository.draw_label_to_image(draw_label)
        return response
