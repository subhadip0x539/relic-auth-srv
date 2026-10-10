from internal.port.auth import AuthService
from internal.dto.auth import (
    PostRegisterRequestBody,
    PostRegisterResponse,
)
from fastapi import HTTPException, status


class AuthHandler:
    svc: AuthService

    def __init__(self, svc: AuthService):
        self.svc = svc

    def register(self, body: PostRegisterRequestBody) -> PostRegisterResponse:
        user = self.svc.register(body.username, body.password)

        if not user:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "User registration failed",
            )

        return PostRegisterResponse(body=f"User registered successfully")
