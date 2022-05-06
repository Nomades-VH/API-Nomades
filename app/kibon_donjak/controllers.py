from fastapi import APIRouter

router = APIRouter(prefix="/kibon_donjak")


# TODO: Create Get method
@router.get("/")
async def get_breakdowns():
    pass


# TODO: Create Get Method
@router.get("/")
async def get_breakdown():
    pass


# TODO: Create Post Method
@router.post("/")
async def create_breakdown():
    pass


# TODO: Create Put Method
@router.put("/")
async def update_breakdown():
    pass


# TODO: Create Delete Method
@router.delete("/")
async def delete_breakdown():
    pass
