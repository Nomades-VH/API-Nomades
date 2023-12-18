from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_400_BAD_REQUEST

from app.auth.exceptions import InvalidCredentials
from app.uow import SqlAlchemyUow
from app.user.models import User
from ports.uow import AbstractUow
from app.auth import services as sv
from app.user import services as user_sv

router = APIRouter(prefix="/auth")

# TODO: Precisamos melhorar todos os controllers


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
        token = await sv.add_token(uow, username, password)

        return {"access_token": token.access_token or token, "token_type": "bearer"}
    except InvalidCredentials:
        return {"status_code": 401, "message": "Credenciais inválidas."}


@router.get("/")
async def get_all(uow: AbstractUow = Depends(SqlAlchemyUow)):
    return list(map(asdict, sv.get_all(uow)))


@router.post("/logout")
async def logout(token: str = Depends(sv.oauth2_scheme), uow: AbstractUow = Depends(SqlAlchemyUow)):
    sv.revoke_token(uow, token)
    return {"status": 200, "detail": "Logout realizado com sucesso"}


@router.put("/refresh-token")
async def refresh_token(
        current_user: User = Depends(sv.get_current_user),
        uow: AbstractUow = Depends(SqlAlchemyUow)
):
    try:

        token = sv.refresh_token(uow=uow, user=current_user)

        return {"access_token": token.access_token, "token_type": "bearer"}

    except HTTPException as e:
        return e
