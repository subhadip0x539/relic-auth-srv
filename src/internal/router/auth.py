from fastapi import APIRouter, Depends, status
from internal.dto.auth import (
    PostRegisterRequestBody,
    PostRegisterResponse,
)
from internal.deps.auth import get_auth_handler, AuthHandler

router = APIRouter(prefix="/auth")


@router.post(
    "/register",
    response_model=PostRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
def register(
    body: PostRegisterRequestBody, hdl: AuthHandler = Depends(get_auth_handler)
):
    return hdl.register(body)
