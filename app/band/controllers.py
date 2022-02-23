from fastapi import APIRouter

router = APIRouter(prefix="/band")

@router.get("/")
async def get_bands():
    return {"band": "Hello from band"}