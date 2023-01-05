from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import RedirectResponse

from app.auth.exceptions import InvalidCredentials
from app.auth.schemas import Credentials
from app.auth.value_object import Token
from app.uow import SqlAlchemyUow
from ports.uow import AbstractUow
from app.auth.services import generate_token

router = APIRouter(prefix="/auth")


@router.post("")
async def login(credentials: Credentials, uow: AbstractUow = Depends(SqlAlchemyUow)):
    try:
        token = generate_token(
            email=credentials.email, password=credentials.password, uow=uow
        )

        return {"token": token.access_token}
    except InvalidCredentials:
        raise HTTPException(status_code=400, detail="Invalid credentials")

# TODO: Criar sistema de logout
@router.post("")
async def logout(token: Token, uow: AbstractUow = Depends(SqlAlchemyUow)):
    ...
