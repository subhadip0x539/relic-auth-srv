from abc import ABC, abstractmethod
from internal.domain.auth import User, Tokens


class AuthRepository(ABC):
    @abstractmethod
    def get_user(self, username: str) -> User | None:
        pass

    @abstractmethod
    def verify_password(self, password_hash: str, password: str) -> bool:
        pass

    @abstractmethod
    def get_dummy_password_hash(self) -> str:
        pass

    @abstractmethod
    def needs_rehash(self, password_hash: str) -> bool:
        pass

    @abstractmethod
    def rehash_password(self, id: str, password: str) -> None:
        pass

    @abstractmethod
    def hash(self, token: str) -> str:
        pass

    @abstractmethod
    def create_refresh_token(self) -> str:
        pass


class AuthService(ABC):
    @abstractmethod
    def authenticate(self, username: str, password: str) -> User | None:
        pass

    @abstractmethod
    def issue_tokens(self, user: User) -> Tokens:
        pass
