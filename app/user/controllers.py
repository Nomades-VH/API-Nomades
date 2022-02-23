from fastapi import APIRouter

router = APIRouter(prefix="/user")

@router.get("/")
async def read_user():
    return {"user": "Hello from user"}