from abc import ABC, abstractmethod
from internal.domain.auth import User, TokenPair, RefreshToken


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
    def create_user(
        self, username: str, password_hash: str, fname: str, lname: str
    ) -> User:
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
        token_hash: str,
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

    @abstractmethod
    def get_refresh_token_by_hash(self, token_hash: str) -> RefreshToken | None:
        pass

    @abstractmethod
    def hash_refresh_token(self, refresh_token: str) -> str:
        pass

    @abstractmethod
    def revoke_family(self, family_id: str) -> None:
        pass


class AuthService(ABC):
    @abstractmethod
    def register(
        self, username: str, password: str, fname: str, lname: str
    ) -> User | None:
        pass

    @abstractmethod
    def login(
        self, username: str, password: str, user_agent: str | None, ip: str | None
    ) -> TokenPair:
        pass

    @abstractmethod
    def refresh(
        self, refresh_token: str | None, user_agent: str | None, ip: str | None
    ) -> TokenPair:
        pass

    @abstractmethod
    def logout(self, refresh_token: str | None) -> None:
        pass

    @abstractmethod
    def me(slef, username: str) -> User | None:
        pass
