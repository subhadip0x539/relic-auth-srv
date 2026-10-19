from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class Permission(str, Enum):
    WORKSPACE_READ = "workspace:read"
    WORKSPACE_CREATE = "workspace:create"

    ENVIRONMENT_READ = "environment:read"
    ENVIRONMENT_CREATE = "environment:create"

    SERVICE_CREATE = "service:create"

    FLAG_CREATE = "flag:create"


class Role(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    READONLY = "readonly"


class User(BaseModel):
    username: str
    fname: str
    lname: str
    password_hash: str
    role: Role = Role.READONLY
    permissions: list[Permission] = [Permission.WORKSPACE_READ]
    is_active: bool
    failed_login_count: int = 0
    locked_until: datetime | None = None
    created_at: datetime
    updated_at: datetime


class TokenClaims(BaseModel):
    sub: str
    role: Role
    permissions: list[Permission]
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
