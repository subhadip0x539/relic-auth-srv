from .response import Response
from pydantic import BaseModel


class PostLoginRequestBody(BaseModel):
    username: str
    password: str


class PostLoginResponseBody(BaseModel):
    access_token: str


PostLoginResponse = Response[PostLoginResponseBody]
