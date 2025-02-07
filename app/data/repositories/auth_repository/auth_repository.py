from app.core.models.login_data import LoginData
from app.data.services.auth_service import AuthService

class AuthRepository:
    def __init__(self, auth_service=None):
        self.auth_service = auth_service or AuthService()
        
    def login(self, login_data: LoginData):
        return self.auth_service.login(login_data=login_data)
    
    def register_user(self, user_data: LoginData):
        return self.auth_service.register_user(user_data)
    
    def refresh(self, refresh_token: str):
        return self.auth_service.refresh_token(refresh_token)
