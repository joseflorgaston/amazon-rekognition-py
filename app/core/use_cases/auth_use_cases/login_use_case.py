from app.core.models.login_data import LoginData
from app.data.repositories.auth_repository.auth_repository import AuthRepository

class LoginUseCase:
    def __init__(self):
        self.auth_repository = AuthRepository()

    def execute(self, login_data: LoginData):
        response = self.auth_repository.login(login_data=login_data)
        return response
