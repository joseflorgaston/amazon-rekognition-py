from app.data.repositories.auth_repository.auth_repository import AuthRepository

class RefreshTokenUseCase:
    def __init__(self):
        self.auth_repository = AuthRepository()

    def execute(self, refresh_token: str):
        response = self.auth_repository.refresh(refresh_token=refresh_token)
        return response
