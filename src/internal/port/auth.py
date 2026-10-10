from abc import ABC, abstractmethod
from internal.domain.auth import User


class AuthRepository(ABC):
    @abstractmethod
    def get_user(self, username: str) -> User | None:
        pass

    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def create_user(self, username: str, password_hash: str) -> User:
        pass


class AuthService(ABC):
    @abstractmethod
    def register(self, username: str, password: str) -> User | None:
        pass
