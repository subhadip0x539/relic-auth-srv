from .response import Response
from pydantic import BaseModel


class PostLoginRequestBody(BaseModel):
    username: str
    password: str


class PostLoginResponseBody(BaseModel):
    access_token: str


PostLoginResponse = Response[PostLoginResponseBody]


class PostRegisterRequestBody(BaseModel):
    fname: str
    lname: str
    username: str
    password: str


PostRegisterResponse = Response[str]


class PostRefreshResponseBody(BaseModel):
    access_token: str


PostRefreshResponse = Response[PostRefreshResponseBody]


class GetMeResponseBody(BaseModel):
    username: str
    fname: str
    lname: str


GetMeResponse = Response[GetMeResponseBody]
