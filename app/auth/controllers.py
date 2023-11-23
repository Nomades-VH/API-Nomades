from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.exceptions import InvalidCredentials
from app.auth.value_object import Token
from app.uow import SqlAlchemyUow
from ports.uow import AbstractUow
from app.auth.services import generate_token

router = APIRouter(prefix="/auth")


# use: form_data: OAuth2PasswordRequestForm = Depends(), para testar no docs fastapi
# use: username: str = Body(...),
# use: password: str = Body(...) para sistemas fora do fastapi
@router.post("")
async def login(
        username: str = Body(...),
        password: str = Body(...),
        uow: AbstractUow = Depends(SqlAlchemyUow)
):
    try:
        token = generate_token(
            username=username, password=password, uow=uow
        )

        return {"access_token": token.access_token, "token_type": "bearer"}
    except InvalidCredentials:
        raise HTTPException(status_code=400, detail="Invalid credentials")


# TODO: Criar sistema de logout
@router.post("")
async def logout(token: Token, uow: AbstractUow = Depends(SqlAlchemyUow)):
    ...
