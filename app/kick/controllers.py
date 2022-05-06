from fastapi import APIRouter

router = APIRouter(prefix="/kick")


# TODO: Create Get Method
@router.get("/")
async def get_kicks():
    pass


# TODO: Create Get Method
@router.get("/")
async def get_kick():
    pass


# TODO: Create Post Method
@router.post("/")
async def post_kick():
    pass


# TODO: Create Put Method
@router.put("/")
async def put_kick():
    pass


# TODO: Create Delete Method
@router.delete("/")
async def delete_kick():
    pass
