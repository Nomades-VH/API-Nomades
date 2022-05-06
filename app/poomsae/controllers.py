from fastapi import APIRouter

router = APIRouter(prefix="/poomsae")


# TODO: Create Get Method
@router.get("/")
async def get_poomsaes():
    pass


# TODO: Create Get Method
@router.get("/")
async def get_poomsae():
    pass


# TODO: Create Post Method
@router.post("/")
async def create_poomsae():
    pass


# TODO: Create Put Method
@router.put("/")
async def update_poomsae():
    pass


# TODO: Create Delete Method
@router.delete("/")
async def delete_poomsae():
    pass
