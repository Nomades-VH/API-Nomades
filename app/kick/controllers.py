from fastapi import APIRouter

router = APIRouter(prefix="/kick")


# TODO: Create Get Method
@router.get("/")
async def get():
    pass


# TODO: Create Get Method
@router.get("/")
async def get_by_id():
    pass


# TODO: Create Post Method
@router.post("/")
async def post():
    pass


# TODO: Create Put Method
@router.put("/")
async def put():
    pass


# TODO: Create Delete Method
@router.delete("/")
async def delete():
    pass
