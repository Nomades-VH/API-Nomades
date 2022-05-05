from fastapi import APIRouter

router = APIRouter(prefix="/kick")


@router.get("/")
def read_root():
    return {"Hello": "Hello from Kick!"}
