from fastapi import APIRouter
from .auth import router as auth_router

v1 = APIRouter(prefix="/v1")

router = APIRouter()

v1.include_router(auth_router)


@router.get("/ping")
def ping():
    return {"message": "pong"}


router.include_router(v1)
