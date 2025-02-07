from datetime import datetime
from app.core.models.camera_data import CameraData
from app.core.models.login_data import LoginData
from app.core.use_cases.auth_use_cases.login_use_case import LoginUseCase
from app.core.use_cases.auth_use_cases.refresh_use_case import RefreshTokenUseCase
from app.core.use_cases.auth_use_cases.register_user_use_case import RegisterUserUseCase

class AuthController:
    @staticmethod
    def login(request):
        login_data = LoginData(
            user=request['username'],
            password=request['password']
        )
        return LoginUseCase().execute(login_data)

    @staticmethod
    def register_user(request):
        user_data = LoginData(
            user=request['username'],
            password=request['password']
        )
        return RegisterUserUseCase().execute(user_data)
    
    @staticmethod
    def refresh(refresh_token: str):
        return RefreshTokenUseCase().execute(refresh_token)
