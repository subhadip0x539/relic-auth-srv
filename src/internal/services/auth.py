from internal.port.auth import AuthService, AuthRepository
from internal.domain.auth import User, Tokens


class AuthServiceImpl(AuthService):
    def __init__(self, repo: AuthRepository):
        self.repo = repo

    def authenticate(self, username: str, password: str) -> User | None:
        user = self.repo.get_user(username)

        password_hash = (
            user.password_hash if user else self.repo.get_dummy_password_hash()
        )

        ok = self.repo.verify_password(password_hash, password) and user is not None

        if not ok or not user or not user.is_active:
            return None

        if self.repo.needs_rehash(user.password_hash):
            self.repo.rehash_password(user.id, user.password_hash)

        return user

    def issue_tokens(self, user: User) -> Tokens:
        return
