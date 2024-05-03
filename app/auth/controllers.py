from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from app.auth.schemas import Credentials
from app.auth.services import get_current_user_with_permission
from app.uow import SqlAlchemyUow
from app.user.models import User
from app.utils.controllers.get_controller import get_controller
from general_enum.permissions import Permissions
from ports.uow import AbstractUow
from app.auth import services as sv
from fastapi import Request

router = APIRouter(prefix="/auth")


# use: form_data: OAuth2PasswordRequestForm = Depends(), para testar no docs fastapi
# use: username: str = Body(...),
# use: password: str = Body(...) para sistemas fora do fastapi
@router.post("")
async def login(
        request: Request,
        credentials: Credentials,
        uow: AbstractUow = Depends(SqlAlchemyUow)
):
    try:
        token = await sv.add(uow, credentials, request.client.host)

        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={
                "access_token": token.access_token,
                "token_type": "bearer"
            }
        )
    except Exception as e:
        print("É aqui é?", e)
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content={"message": "Credenciais inválidas."})


@router.get("/")
@get_controller(sv)
async def get(
        message_error: str = "Tokens não encontrados.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.root))
):
    ...


@router.post("/logout")
async def logout(request: Request,
                 current_user: User = Depends(get_current_user_with_permission(Permissions.student)),
                 uow: AbstractUow = Depends(SqlAlchemyUow)):

    response = sv.revoke_token(uow, current_user, request.client.host)
    if response:
        return response

    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "Logout realizado com sucesso."})


@router.put("/refresh-token")
async def refresh_token(
        request: Request,
        token: str = Depends(sv.oauth2_scheme),
        current_user: User = Depends(sv.get_current_user_with_permission(Permissions.student)),
        uow: AbstractUow = Depends(SqlAlchemyUow)
):
    try:
        token = sv.refresh_token(uow=uow, token=token, user=current_user, ip_user=request.client.host)
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={
                "access_token": token.access_token,
                "token_type": "Bearer"
            }
        )
    except HTTPException as e:
        return e
