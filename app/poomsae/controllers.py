from fastapi import APIRouter

router = APIRouter(prefix="/poomsae")


@router.get("/")
def read_root():
    return {"Hello": "Hello from Poomsae"}
