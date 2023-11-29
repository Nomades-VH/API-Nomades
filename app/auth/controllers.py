from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.exceptions import InvalidCredentials
from app.uow import SqlAlchemyUow
from app.user.models import User
from ports.uow import AbstractUow
from app.auth import services as sv

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
    # TODO: O usuário pode fazer quantos logins quiser, criando assim vários tokens, e mesmo já estando logado
    try:
        token = sv.add_token(uow, username, password)

        return {"access_token": token.access_token, "token_type": "bearer"}
    except InvalidCredentials:
        return {"status_code": 401, "message": "Credenciais inválidas."}


# TODO: Criar sistema de logout
@router.post("/logout")
async def logout(token: str = Depends(sv.oauth2_scheme)):
    # sv.add_token_blacklist(token)
    return {"status": 200, "detail": "Logout realizado com sucesso"}


@router.post("/refresh-token")
async def refresh_token(
        current_user: User = Depends(sv.get_current_user),
        auth: str = Depends(sv.oauth2_scheme)
):
    try:

        # token = sv.refresh_token(user=current_user, token=auth)

        return {"access_token": 'asd', "token_type": "bearer"}

    except HTTPException as e:
        return e
