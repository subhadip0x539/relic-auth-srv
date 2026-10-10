from fastapi import APIRouter, Depends
from internal.dto.auth import PostLoginResponse, PostLoginRequestBody
from internal.deps.auth import get_auth_handler, AuthHandler

router = APIRouter(prefix="/auth")


@router.post(
    "/login", response_model=PostLoginResponse, response_model_exclude_none=True
)
def login(body: PostLoginRequestBody, hdl: AuthHandler = Depends(get_auth_handler)):
    return hdl.login(body)
