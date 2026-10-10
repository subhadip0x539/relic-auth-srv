from internal.port.auth import AuthService, AuthRepository
from internal.domain.auth import User
from fastapi import HTTPException, status


class AuthServiceImpl(AuthService):
    def __init__(self, repo: AuthRepository):
        self.repo = repo

    def register(self, username: str, password: str) -> User | None:
        if self.repo.get_user(username):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Username already taken",
            )

        password_hash = self.repo.hash_password(password)

        user = self.repo.create_user(username, password_hash)

        return user
