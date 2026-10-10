from internal.infra.mongo import MongoClient
from config import config
from argon2 import PasswordHasher

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
