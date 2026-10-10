from internal.port.auth import AuthRepository
from pymongo.database import Database
from typing import Any
from internal.domain.auth import User
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from uuid import uuid4


class AuthRepositoryImpl(AuthRepository):
    def __init__(self, db: Database[Any], password_hasher: PasswordHasher):
        self._db = db
        self.password_hasher = password_hasher
        self._dummy = password_hasher.hash(str(uuid4()))

    def get_user(self, username: str) -> User | None:
        collection = self._db.get_collection("users")

        doc = collection.find_one({"username": username.strip().lower()})

        if not doc:
            return None

        return User(
            id=doc["_id"],
            username=doc["username"],
            password_hash=doc["password_hash"],
            roles=doc["roles"],
            is_active=doc["is_active"],
            token_version=doc["token_version"],
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
        )

    def hash(self, token: str) -> str:
        return self.password_hasher.hash(token)

    def verify_password(self, password_hash: str, password: str) -> bool:
        try:
            return self.password_hasher.verify(password_hash, password)
        except (VerifyMismatchError, InvalidHashError):
            return False

    def get_dummy_password_hash(self) -> str:
        return self._dummy

    def needs_rehash(self, password_hash: str) -> bool:
        try:
            return self.password_hasher.check_needs_rehash(password_hash)
        except InvalidHashError:
            return True

    def rehash_password(self, id: str, password: str) -> None:
        collection = self._db.get_collection("users")

        collection.update_one(
            {"_id": id},
            {"$set": {"password_hash": self.hash(password)}},
        )
