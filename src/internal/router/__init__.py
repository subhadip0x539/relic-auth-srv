from fastapi import APIRouter

v1 = APIRouter(prefix="/v1")

router = APIRouter()


@router.get("/ping")
def ping():
    return {"message": "pong"}


router.include_router(v1)
