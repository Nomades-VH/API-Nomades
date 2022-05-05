from fastapi import APIRouter

router = APIRouter(prefix="/kibon_donjak")


@router.get("/")
async def root():
    return {"message": "Hello from Kibon Donjak"}
