from fastapi import APIRouter

router = APIRouter(prefix="/theory")

@router.get("/")
async def get_theory():
    return {"message": "Hello from theory"}