from internal.port.auth import AuthRepository
from pymongo.database import Database
from typing import Any
from internal.domain.auth import User, Role
from argon2 import PasswordHasher
from datetime import datetime


class AuthRepositoryImpl(AuthRepository):
    def __init__(self, db: Database[Any], password_hasher: PasswordHasher):
        self._db = db
        self.password_hasher = password_hasher

    def get_user(self, username: str) -> User | None:
        collection = self._db.get_collection("users")

        doc = collection.find_one({"username": username})

        if not doc:
            return None

        return User(
            username=doc["username"],
            password_hash=doc["password_hash"],
            roles=doc["roles"],
            is_active=doc["is_active"],
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
        )

    def hash_password(self, password: str) -> str:
        return self.password_hasher.hash(password)

    def create_user(self, username: str, password_hash: str) -> User:
        collection = self._db.get_collection("users")

        user = User(
            username=username,
            password_hash=password_hash,
            roles=[Role.VIEWER],
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        collection.insert_one(user.model_dump())

        return user
