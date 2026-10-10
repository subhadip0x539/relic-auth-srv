from typing import TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    detail: Optional[str] = None
    body: T
