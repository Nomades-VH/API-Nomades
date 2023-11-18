from fastapi import APIRouter, Depends, HTTPException
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
        form_data: OAuth2PasswordRequestForm = Depends(),
        uow: AbstractUow = Depends(SqlAlchemyUow)
):
    try:
        token = generate_token(
            username=form_data.username, password=form_data.password, uow=uow
        )

        return {"access_token": token.access_token, "token_type": "bearer"}
    except InvalidCredentials:
        raise HTTPException(status_code=400, detail="Invalid credentials")


# TODO: Criar sistema de logout
@router.post("")
async def logout(token: Token, uow: AbstractUow = Depends(SqlAlchemyUow)):
    ...
