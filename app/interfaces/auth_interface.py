from abc import ABC, abstractmethod

from app.core.models.login_data import LoginData

class AuthInterface(ABC):
    @abstractmethod
    def login(self, camera_id: str):
        pass

    @abstractmethod
    def register_user(self, login_data: LoginData):
        pass
    
    @abstractmethod
    def refresh_token(self, refresh_token: str):
        pass
