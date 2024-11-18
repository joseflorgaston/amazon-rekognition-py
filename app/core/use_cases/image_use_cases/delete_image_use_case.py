from app.data.repositories.image_repository.image_repository import ImageRepository

class DeleteImageUseCase:
    def __init__(self):
        self.image_repository = ImageRepository()

    def execute(self, image_id: str):
        response = self.image_repository.delete_image(image_id)
        return response
