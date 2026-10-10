import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings
from typing import TypedDict

DEFAULT_MONGO_URI = "mongodb://user:P@ssw0Rd!@localhost:22017"
DEFAULT_MONGO_DATABASE_NAME = "relic_core"

DEFAULT_SERVER_HOST = "localhost"
DEFAULT_SERVER_PORT = 8081


class ServerData(TypedDict, total=False):
    host: str
    port: int


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


class ConfigBuilder:

    def __init__(self):
        self._server_data: ServerData = {}
        self._mongo_data: MongoData = {}

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
                    "MONGO_DATABASE", DEFAULT_MONGO_DATABASE_NAME
                ),
            }
        )

        return self

    def server(
        self, host: str = DEFAULT_SERVER_HOST, port: int = DEFAULT_SERVER_PORT
    ) -> "ConfigBuilder":
        self._server_data.update({"host": host, "port": port})
        return self

    def temporal(
        self, uri: str = DEFAULT_MONGO_URI, database: str = DEFAULT_MONGO_DATABASE_NAME
    ) -> "ConfigBuilder":
        self._mongo_data.update({"uri": uri, "database_name": database})
        return self

    def build(self) -> Config:
        return Config(
            server=Server(**self._server_data), mongo=Mongo(**self._mongo_data)
        )
