from internal.port.auth import AuthService
from internal.dto.auth import (
    PostRegisterRequestBody,
    PostRegisterResponse,
    PostLoginRequestBody,
    PostLoginResponseBody,
    PostLoginResponse,
    PostRefreshResponseBody,
    PostRefreshResponse,
    GetMeResponseBody,
    GetMeResponse,
)
from fastapi import HTTPException, status, Request, Response
from internal.domain.error import (
    InvalidCredentialsError,
    AccountLockedError,
    InvalidTokenError,
)
from internal.lib.claims import Claims


class AuthHandler:
    svc: AuthService

    def __init__(self, svc: AuthService):
        self.svc = svc

    def register(self, body: PostRegisterRequestBody) -> PostRegisterResponse:
        result = self.svc.register(body.username, body.password, body.fname, body.lname)

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
            path="/v1/auth",
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
            path="/v1/auth",
        )

        return PostRefreshResponse(
            body=PostRefreshResponseBody(access_token=result.access_token)
        )

    def me(self, claims: Claims) -> GetMeResponse:

        result = self.svc.me(claims.sub)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        return GetMeResponse(
            body=GetMeResponseBody(
                username=result.username, fname=result.fname, lname=result.lname
            )
        )

    def logout(self, refresh_token: str | None, response: Response) -> None:
        try:
            self.svc.logout(refresh_token)
        except InvalidTokenError as exc:
            raise HTTPException(exc.code, exc.message)

        response.delete_cookie(
            key="refresh_token",
            path="/v1/auth",
            httponly=True,
            secure=False,
            samesite="lax",
        )
