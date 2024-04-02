from http import HTTPStatus
from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse, Response

from app.auth.services import get_current_user_with_permission
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.user.exceptions import UserException
from app.user.models import User as ModelUser
from app.user import services as sv
from app.utils.controllers.delete_controller import delete_controller
from app.utils.controllers.get_controller import get_controller
from general_enum.permissions import Permissions
from ports.uow import AbstractUow

router = APIRouter(prefix="/user")


# TODO: Verify methods
@router.post("/")
async def create_user(
        user: ModelUser,
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.table))
) -> Response:
    try:
        user = sv.change_user(user)
        if not sv.verify_if_user_exists(uow, user):
            if user.permission.value >= Permissions.table.value and current_user.permission.value < Permissions.root.value:
                return JSONResponse(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    content={"message": "Não é possível criar um usuário com essa permissão."}
                )
            sv.create_new_user(uow, user, current_user)
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content=jsonable_encoder(user)
            )
        else:
            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content={"message": "Esse usuário já existe."}
            )
    except UserException:
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"message": "Não foi possível criar usuário. Tente novamente mais tarde."}
        )


# TODO: Deve retornar também o token de acesso do usuário
@router.get("/me/")
async def get_me(current_user: User = Depends(get_current_user_with_permission(Permissions.student))):
    return current_user


@router.get('/')
@get_controller(sv)
async def get(
        message_error: str = "Não foi possível pegar os usuários",
        current_user: User = Depends(get_current_user_with_permission(Permissions.table)),
        uow: AbstractUow = Depends(SqlAlchemyUow)
):
    ...


# TODO: Create Update Method
async def update_user(
        current_user: User = Depends(get_current_user_with_permission(Permissions.table)),
        uow: AbstractUow = Depends(SqlAlchemyUow)
):
    ...


# TODO: Create Delete Method
@router.delete('/{uuid}')
@delete_controller(sv)
async def delete_user(
        uuid: UUID,
        message_success: str = "Usuário deletado com sucesso.",
        message_error: str = "Não foi possível deletar o usuário.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.table))
):
    ...
