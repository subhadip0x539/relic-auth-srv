from internal.port.auth import AuthRepository
from pymongo.database import Database
from typing import Any
from internal.domain.auth import User, Role, Claims
from argon2 import PasswordHasher
from datetime import datetime, timezone, timedelta
from uuid import uuid4
import hashlib, secrets
import jwt


class AuthRepositoryImpl(AuthRepository):
    def __init__(
        self,
        db: Database[Any],
        password_hasher: PasswordHasher,
        secret: str,
        algorithm: str,
        access_ttl_seconds: int,
        refresh_ttl_seconds: int,
        lockout_duration_seconds: int,
        max_login_attempts: int,
    ):
        self._db = db
        self._users_collection = self._db.get_collection("users")
        self._refresh_tokens_collection = self._db.get_collection("refresh_tokens")
        self._password_hasher = password_hasher
        self._secret = secret
        self._algorithm = algorithm
        self._access_ttl_seconds = access_ttl_seconds
        self._refresh_ttl_seconds = refresh_ttl_seconds
        self._lockout_duration_seconds = lockout_duration_seconds
        self._max_login_attempts = max_login_attempts

    def get_user(self, username: str) -> User | None:
        doc = self._users_collection.find_one({"username": username})

        if not doc:
            return None

        return User(
            username=doc["username"],
            password_hash=doc["password_hash"],
            roles=doc["roles"],
            is_active=doc["is_active"],
            locked_until=doc["locked_until"],
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
            failed_login_count=doc["failed_login_count"],
        )

    def hash_password(self, password: str) -> str:
        return self._password_hasher.hash(password)

    def verify_password(self, password: str, password_hash: str) -> bool:
        try:
            return self._password_hasher.verify(password_hash, password)
        except Exception:
            return False

    def create_user(self, username: str, password_hash: str) -> User:

        user = User(
            username=username,
            password_hash=password_hash,
            roles=[Role.VIEWER],
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        self._users_collection.insert_one(user.model_dump())

        return user

    def record_failed_login(self, username: str) -> None:
        doc = self._users_collection.find_one_and_update(
            {"username": username},
            {"$inc": {"failed_login_count": 1}},
            return_document=True,
        )

        if doc and doc["failed_login_count"] >= self._max_login_attempts:
            self._users_collection.update_one(
                {"username": username},
                {
                    "$set": {
                        "locked_until": datetime.now(timezone.utc)
                        + timedelta(seconds=self._lockout_duration_seconds),
                        "failed_login_count": 0,
                    }
                },
            )

    def record_successful_login(self, username: str) -> None:
        self._users_collection.update_one(
            {"username": username},
            {
                "$set": {
                    "failed_login_count": 0,
                    "locked_until": None,
                }
            },
        )

    def check_needs_rehash(self, password_hash: str) -> bool:
        return self._password_hasher.check_needs_rehash(password_hash)

    def rehash_password(self, username: str, password_hash: str) -> None:
        self._users_collection.update_one(
            {"username": username},
            {
                "$set": {
                    "password_hash": password_hash,
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )

    def new_access_token(self, user: User) -> str:
        now = datetime.now(timezone.utc)

        claims = Claims(
            sub=user.username,
            roles=user.roles,
            jti=str(uuid4()),
            iat=now,
            exp=now + timedelta(seconds=self._access_ttl_seconds),
        )

        token: str = jwt.encode(claims.model_dump(), key=self._secret, algorithm=self._algorithm)  # type: ignore

        return token

    def new_refresh_token(self) -> tuple[str, str, int]:
        raw = secrets.token_urlsafe(48)

        return raw, hashlib.sha256(raw.encode()).hexdigest(), self._refresh_ttl_seconds

    def create_refresh_token(
        self,
        username: str,
        refresh_hash: str,
        family_id: str,
        user_agent: str | None,
        ip: str | None,
    ) -> None:
        now = datetime.now(timezone.utc)

        collection = self._db.get_collection("refresh_tokens")

        collection.insert_one(
            {
                "user_id": username,
                "token_hash": refresh_hash,
                "family_id": family_id,
                "issued_at": now,
                "expires_at": now + timedelta(seconds=self._refresh_ttl_seconds),
                "revoked_at": None,
                "replaced_by": None,
                "user_agent": user_agent,
                "ip": ip,
            }
        )
