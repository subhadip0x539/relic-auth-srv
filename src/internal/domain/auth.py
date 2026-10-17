from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    MANAGER = "manager"
    VIEWER = "viewer"


class User(BaseModel):
    username: str
    password_hash: str
    roles: list[Role] = [Role.VIEWER]
    is_active: bool
    failed_login_count: int = 0
    locked_until: datetime | None = None
    created_at: datetime
    updated_at: datetime


class Claims(BaseModel):
    sub: str
    roles: list[Role]
    jti: str
    iat: datetime
    exp: datetime


class RefreshToken(BaseModel):
    username: str
    token_hash: str
    family_id: str
    issued_at: datetime
    expires_at: datetime
    revoked_at: datetime | None = None
    user_agent: str | None
    ip: str | None


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    refresh_ttl_seconds: int
