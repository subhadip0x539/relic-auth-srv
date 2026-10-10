from typing import Optional
from pymongo import MongoClient as PyMongoClient
from pymongo.database import Database
from typing import Any


class MongoClient:
    def __init__(self) -> None:
        self._uri: Optional[str] = None
        self._database_name: Optional[str] = None
        self._client: Optional[PyMongoClient[Any]] = None
        self._db: Optional[Database[Any]] = None

    def uri(self, uri: str) -> "MongoClient":
        self._uri = uri
        return self

    def database_name(self, database_name: str) -> "MongoClient":
        self._database_name = database_name
        return self

    def connect(self) -> "MongoClient":
        if not self._uri:
            raise ValueError("URI is required")
        if not self._database_name:
            raise ValueError("Database name is required")

        self._client = PyMongoClient(self._uri)

        self._db = self._client[self._database_name]

        return self

    def disconnect(self):
        if self._client is not None:
            self._client.close()
            self._client = None
            self._db = None

    @property
    def db(self) -> Database[Any]:
        if self._db is None:
            raise RuntimeError("Not connected")
        return self._db
