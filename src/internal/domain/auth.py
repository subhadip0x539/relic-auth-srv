from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    MANAGER = "manager"
    VIEWER = "viewer"


class User(BaseModel):
    id: str
    username: str
    password_hash: str
    roles: list[Role] = [Role.VIEWER]
    is_active: bool
    token_version: int
    created_at: datetime
    updated_at: datetime


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
