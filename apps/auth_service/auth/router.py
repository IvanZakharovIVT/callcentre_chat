from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign_up")
async def sign_up():
    ...