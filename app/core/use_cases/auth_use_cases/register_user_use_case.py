from app.core.models.login_data import LoginData
from app.data.repositories.auth_repository.auth_repository import AuthRepository

class RegisterUserUseCase:
    def __init__(self):
        self.auth_repository = AuthRepository()

    def execute(self, register_user: LoginData):
        response = self.auth_repository.register_user(user_data=register_user)
        return response
