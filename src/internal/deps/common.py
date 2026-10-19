from internal.infra.mongo import MongoClient
from config import config
from argon2 import PasswordHasher
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from internal.domain.error import InvalidTokenError
from internal.lib.claims import Claims

mongo_client = (
    MongoClient()
    .uri(config.mongo.uri)
    .database_name(config.mongo.database_name)
    .connect()
)


def get_mongo_client() -> MongoClient:
    return mongo_client


password_hasher = PasswordHasher()


def get_password_hasher() -> PasswordHasher:
    return password_hasher


bearer = HTTPBearer(auto_error=False)


def get_claims(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> Claims:
    if not creds:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
    try:
        return Claims(creds.credentials, config.auth.secret, config.auth.algorithm)
    except InvalidTokenError as exc:
        raise HTTPException(exc.code, exc.message)
