import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings
from typing import TypedDict

DEFAULT_MONGO_URI = "mongodb://user:P@ssw0Rd!@localhost:22017"
DEFAULT_MONGO_DATABASE_NAME = "relic_auth"

DEFAULT_SERVER_HOST = "localhost"
DEFAULT_SERVER_PORT = 8081

DEFAULT_AUTH_SECRET = "secret"
DEFAULT_AUTH_ALGORITHM = "HS256"
DEFAULT_AUTH_ACCESS_TTL_SECONDS = 900
DEFAULT_AUTH_REFRESH_TTL_SECONDS = 604800
DEFAULT_AUTH_MAX_LOGIN_ATTEMPTS = 5
DEFAULT_AUTH_LOCKOUT_DURATION_SECONDS = 900


class AuthData(TypedDict, total=False):
    secret: str
    algorithm: str
    access_ttl_seconds: int
    refresh_ttl_seconds: int
    max_login_attempts: int
    lockout_duration_seconds: int


class ServerData(TypedDict, total=False):
    host: str
    port: int


class Auth(BaseSettings):
    secret: str = Field(default=DEFAULT_AUTH_SECRET)
    algorithm: str = Field(default=DEFAULT_AUTH_ALGORITHM)
    access_ttl_seconds: int = Field(default=DEFAULT_AUTH_ACCESS_TTL_SECONDS)
    refresh_ttl_seconds: int = Field(default=DEFAULT_AUTH_REFRESH_TTL_SECONDS)
    max_login_attempts: int = Field(default=DEFAULT_AUTH_MAX_LOGIN_ATTEMPTS)
    lockout_duration_seconds: int = Field(default=DEFAULT_AUTH_LOCKOUT_DURATION_SECONDS)


class Server(BaseSettings):
    host: str = Field(default=DEFAULT_SERVER_HOST)
    port: int = Field(default=DEFAULT_SERVER_PORT)


class MongoData(TypedDict, total=False):
    uri: str
    database_name: str


class Mongo(BaseSettings):
    uri: str = Field(default=DEFAULT_MONGO_URI)
    database_name: str = Field(default=DEFAULT_MONGO_DATABASE_NAME)


class Config(BaseSettings):
    server: Server = Field(default_factory=Server)
    mongo: Mongo = Field(default_factory=Mongo)
    auth: Auth = Field(default_factory=Auth)


class ConfigBuilder:

    def __init__(self):
        self._server_data: ServerData = {}
        self._mongo_data: MongoData = {}
        self._auth_data: AuthData = {}

    def env(self, file: str = ".env") -> "ConfigBuilder":
        load_dotenv(os.path.join(os.getcwd(), file))

        self._server_data.update(
            {
                "host": os.getenv("SERVER_HOST", DEFAULT_SERVER_HOST),
                "port": int(os.getenv("SERVER_PORT", DEFAULT_SERVER_PORT)),
            }
        )

        self._mongo_data.update(
            {
                "uri": os.getenv("MONGO_URI", DEFAULT_MONGO_URI),
                "database_name": os.getenv(
                    "MONGO_DATABASE_NAME", DEFAULT_MONGO_DATABASE_NAME
                ),
            }
        )

        self._auth_data.update(
            {
                "secret": os.getenv("AUTH_SECRET", DEFAULT_AUTH_SECRET),
                "algorithm": os.getenv("AUTH_ALGORITHM", DEFAULT_AUTH_ALGORITHM),
                "access_ttl_seconds": int(
                    os.getenv(
                        "AUTH_ACCESS_TTL_SECONDS", DEFAULT_AUTH_ACCESS_TTL_SECONDS
                    )
                ),
                "refresh_ttl_seconds": int(
                    os.getenv(
                        "AUTH_REFRESH_TTL_SECONDS", DEFAULT_AUTH_REFRESH_TTL_SECONDS
                    )
                ),
                "max_login_attempts": int(
                    os.getenv("AUTH_MAX_ATTEMPTS", DEFAULT_AUTH_MAX_LOGIN_ATTEMPTS)
                ),
                "lockout_duration_seconds": int(
                    os.getenv(
                        "AUTH_LOCKOUT_DURATION_SECONDS",
                        DEFAULT_AUTH_LOCKOUT_DURATION_SECONDS,
                    )
                ),
            }
        )

        return self

    def build(self) -> Config:
        return Config(
            server=Server(**self._server_data),
            mongo=Mongo(**self._mongo_data),
            auth=Auth(**self._auth_data),
        )
