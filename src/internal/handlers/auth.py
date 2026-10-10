from internal.port.auth import AuthService
from internal.dto.auth import (
    PostLoginResponse,
    PostLoginRequestBody,
    PostLoginResponseBody,
)
from fastapi import HTTPException, status


class AuthHandler:
    svc: AuthService

    def __init__(self, svc: AuthService):
        self.svc = svc

    def login(self, body: PostLoginRequestBody) -> PostLoginResponse:
        user = self.svc.authenticate(body.username, body.password)

        if not user:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        tokens = self.svc.issue_tokens(user, meta)

        return PostLoginResponse(body=PostLoginResponseBody(access_token=""))
