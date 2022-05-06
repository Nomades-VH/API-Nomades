from fastapi import APIRouter

router = APIRouter(prefix="/stretching")


# TODO: Create Get Method
@router.get("/")
async def get_stretchings():
    pass


# TODO: Create Get Method
@router.get("/")
async def get_stretching():
    pass


# TODO: Create Post Method
@router.post("/")
async def post_stretching():
    pass


# TODO: Create Put Method
@router.put("/")
async def put_stretching():
    pass


# TODO: Create Delete Method
@router.delete("/")
async def delete_stretching():
    pass
