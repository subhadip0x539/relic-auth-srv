from internal.port.auth import AuthService
from internal.dto.auth import (
    PostRegisterRequestBody,
    PostRegisterResponse,
    PostLoginRequestBody,
    PostLoginResponseBody,
    PostLoginResponse,
    PostRefreshResponseBody,
    PostRefreshResponse,
)
from fastapi import HTTPException, status, Request, Response
from internal.domain.error import (
    InvalidCredentialsError,
    AccountLockedError,
    InvalidTokenError,
)


class AuthHandler:
    svc: AuthService

    def __init__(self, svc: AuthService):
        self.svc = svc

    def register(self, body: PostRegisterRequestBody) -> PostRegisterResponse:
        result = self.svc.register(body.username, body.password)

        if not result:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "User registration failed",
            )

        return PostRegisterResponse(body=f"User registered successfully")

    def login(
        self,
        body: PostLoginRequestBody,
        request: Request,
        response: Response,
    ) -> PostLoginResponse:
        try:
            result = self.svc.login(
                body.username,
                body.password,
                request.headers.get("user-agent"),
                request.client.host if request.client else None,
            )
        except InvalidCredentialsError as exc:
            raise HTTPException(exc.code, exc.message)
        except AccountLockedError as exc:
            raise HTTPException(exc.code, exc.message)

        response.set_cookie(
            key="refresh_token",
            value=result.refresh_token,
            max_age=result.refresh_ttl_seconds,
            httponly=True,
            secure=False,
            samesite="lax",
            path="/auth",
        )

        return PostLoginResponse(
            body=PostLoginResponseBody(access_token=result.access_token)
        )

    def refresh(
        self, refresh_token: str | None, request: Request, response: Response
    ) -> PostRefreshResponse:
        try:
            result = self.svc.refresh(
                refresh_token,
                user_agent=request.headers.get("user-agent"),
                ip=request.client.host if request.client else None,
            )
        except InvalidTokenError as exc:
            raise HTTPException(exc.code, exc.message)

        response.set_cookie(
            key="refresh_token",
            value=result.refresh_token,
            max_age=result.refresh_ttl_seconds,
            httponly=True,
            secure=False,
            samesite="lax",
            path="/auth",
        )

        return PostRefreshResponse(
            body=PostRefreshResponseBody(access_token=result.access_token)
        )
