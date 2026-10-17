from internal.port.auth import AuthService, AuthRepository
from internal.domain.auth import User, TokenPair
from fastapi import HTTPException, status
from internal.domain.error import (
    InvalidCredentialsError,
    AccountLockedError,
    InvalidTokenError,
)
from uuid import uuid4
from datetime import datetime, timezone


class AuthServiceImpl(AuthService):
    def __init__(self, repo: AuthRepository):
        self.repo = repo
        self._dummy_password_hash = repo.hash_password(str(uuid4()))

    def register(self, username: str, password: str) -> User | None:
        if self.repo.get_user(username):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Username already taken",
            )

        password_hash = self.repo.hash_password(password)

        user = self.repo.create_user(username, password_hash)

        return user

    def login(
        self, username: str, password: str, user_agent: str | None, ip: str | None
    ) -> TokenPair:
        user = self.repo.get_user(username)

        password_hash = user.password_hash if user else self._dummy_password_hash

        ok = self.repo.verify_password(password, password_hash)

        if not user or not user.is_active:
            raise InvalidCredentialsError()

        now = datetime.now(timezone.utc)

        if user.locked_until and user.locked_until > now:
            raise AccountLockedError()

        if not ok:
            self.repo.record_failed_login(username)
            raise InvalidCredentialsError()

        if self.repo.check_needs_rehash(user.password_hash):
            self.repo.rehash_password(username, self.repo.hash_password(password))

        self.repo.record_successful_login(username)

        refresh_token, refresh_token_hash, refresh_ttl_seconds = (
            self.repo.new_refresh_token()
        )
        self.repo.create_refresh_token(
            user.username, refresh_token_hash, str(uuid4()), user_agent, ip
        )

        access_token = self.repo.new_access_token(user)

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            refresh_ttl_seconds=refresh_ttl_seconds,
        )

    def refresh(
        self, refresh_token: str | None, user_agent: str | None, ip: str | None
    ) -> TokenPair:
        if not refresh_token:
            raise InvalidTokenError()

        now = datetime.now(timezone.utc)

        token = self.repo.get_refresh_token_by_hash(
            self.repo.hash_refresh_token(refresh_token)
        )

        if not token:
            raise InvalidTokenError()

        if token.revoked_at:
            self.repo.revoke_family(token.family_id)
            raise InvalidTokenError()

        if token.expires_at <= now:
            raise InvalidTokenError()

        user = self.repo.get_user(str(token.username))
        if not user or not user.is_active:
            self.repo.revoke_family(token.family_id)
            raise InvalidTokenError()

        new_refresh_token, new_refresh_token_hash, _refresh_ttl_seconds = (
            self.repo.new_refresh_token()
        )
        self.repo.create_refresh_token(
            token.username,
            new_refresh_token_hash,
            token.family_id,
            user_agent,
            ip,
        )

        access_token = self.repo.new_access_token(user)

        return TokenPair(
            access_token=access_token,
            refresh_token=new_refresh_token,
            refresh_ttl_seconds=_refresh_ttl_seconds,
        )
