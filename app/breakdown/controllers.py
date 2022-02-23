from fastapi import APIRouter

router = APIRouter(prefix="/breakdown")


@router.get("/")
async def get_breakdowns():
    return {"message": "Hello from breakdown"}