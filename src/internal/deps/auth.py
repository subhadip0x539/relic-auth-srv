from .common import MongoClient, get_mongo_client, PasswordHasher, get_password_hasher
from fastapi import Depends
from internal.repositories.auth import AuthRepository, AuthRepositoryImpl
from internal.services.auth import AuthService, AuthServiceImpl
from internal.handlers.auth import AuthHandler


def get_auth_repository(
    mongo_client: MongoClient = Depends(get_mongo_client),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> AuthRepository:
    return AuthRepositoryImpl(mongo_client.db, password_hasher)


def get_auth_service(
    repo: AuthRepository = Depends(get_auth_repository),
) -> AuthService:
    return AuthServiceImpl(repo)


def get_auth_handler(
    svc: AuthService = Depends(get_auth_service),
) -> AuthHandler:
    return AuthHandler(svc)
