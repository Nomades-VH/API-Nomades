from fastapi import APIRouter

router = APIRouter(prefix="/stretching")


@router.get("/")
async def read_root():
    return {"Hello": "Hello from Stretching"}
