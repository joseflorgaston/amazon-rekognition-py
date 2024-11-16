from app.data.repositories.image_repository.image_repository import ImageRepository

class GetLastImageUseCase:
    def __init__(self):
        self.image_repository = ImageRepository()

    def execute(self, camera_id: str):
        response = self.image_repository.get_last_image(camera_id)
        return response
