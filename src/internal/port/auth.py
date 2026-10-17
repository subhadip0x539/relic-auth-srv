from abc import ABC, abstractmethod
from internal.domain.auth import User, TokenPair


class AuthRepository(ABC):
    @abstractmethod
    def get_user(self, username: str) -> User | None:
        pass

    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, password: str, password_hash: str) -> bool:
        pass

    @abstractmethod
    def create_user(self, username: str, password_hash: str) -> User:
        pass

    @abstractmethod
    def new_access_token(self, user: User) -> str:
        pass

    @abstractmethod
    def new_refresh_token(self) -> tuple[str, str, int]:
        pass

    @abstractmethod
    def create_refresh_token(
        self,
        username: str,
        refresh_hash: str,
        family_id: str,
        user_agent: str | None,
        ip: str | None,
    ) -> None:
        pass

    @abstractmethod
    def record_failed_login(self, username: str) -> None:
        pass

    @abstractmethod
    def record_successful_login(self, username: str) -> None:
        pass

    @abstractmethod
    def check_needs_rehash(self, password_hash: str) -> bool:
        pass

    @abstractmethod
    def rehash_password(self, username: str, password_hash: str) -> None:
        pass


class AuthService(ABC):
    @abstractmethod
    def register(self, username: str, password: str) -> User | None:
        pass

    @abstractmethod
    def login(
        self, username: str, password: str, user_agent: str | None, ip: str | None
    ) -> TokenPair:
        pass
