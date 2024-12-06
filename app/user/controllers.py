from http import HTTPStatus
from io import BytesIO
from pathlib import Path
from typing import Optional
from uuid import UUID

from click import confirm
from fastapi import (APIRouter, Depends, File, Form, HTTPException, Request,
                     UploadFile)
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse, Response, StreamingResponse

from app.auth.schemas import Credentials
from app.auth.services import get_current_user_with_permission
from app.uow import SqlAlchemyUow
from app.user import services as sv
from app.user.entities import User
from app.user.exceptions import UserException
from app.user.models import User as ModelUser
from app.utils.controllers.delete_controller import delete_controller
from app.utils.controllers.get_by_controller import get_by_controller
from app.utils.controllers.get_controller import get_controller
from general_enum.hubs import Hubs
from general_enum.permissions import Permissions
from ports.uow import AbstractUow

router = APIRouter(prefix='/user')


# TODO: Verify methods
@router.post('/')
async def create_user(
    request: Request,
    username: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    permission: int = Form(...),
    hub: str = Form(...),
    fk_band: Optional[UUID] = Form(None),
    profile: UploadFile = File(...),
    uow: AbstractUow = Depends(SqlAlchemyUow),
) -> Response:
    formdata = await request.form()

    credentials = Credentials(
        username=username,
        email=email,
        password=password,
    )

    user = ModelUser(
        credentials=credentials,
        permission=permission,
        hub=hub,
        fk_band=fk_band,
    )

    try:
        if user.credentials.password != confirm_password:
            return JSONResponse(
                status_code=HTTPStatus.UNAUTHORIZED,
                content={
                    'message': 'Não foi possível criar um usuário. Senhas não coincidem.'
                },
            )

        user = sv.change_user(user)
        if not sv.verify_if_user_exists(uow, user):
            file_location = await sv.create_src_profile(profile, user)

            user.src_profile = str(file_location)

            sv.create_new_user(uow, user)
            return JSONResponse(
                status_code=HTTPStatus.CREATED, content=jsonable_encoder(user)
            )
        else:
            return JSONResponse(
                status_code=HTTPStatus.CONFLICT,
                content={'message': 'Esse usuário já existe.'},
            )
    except UserException as error:
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={'message': jsonable_encoder(error.message)},
        )


# TODO: Criar entrypoint de envio de imagem do perfil do usuário
@router.put('/profile')
async def upload_image_profile(
    profile: UploadFile = File(...),
    uow: AbstractUow = Depends(SqlAlchemyUow),
    current_user: User = Depends(
        get_current_user_with_permission(Permissions.student)
    ),
):
    file_location = await sv.create_src_profile(profile, current_user)

    with uow:
        current_user.src_profile = str(file_location)
        sv.update_user(uow, current_user)

        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={'message': 'Upload realizado.'},
        )


@router.put('/')
async def update_user(
    uuid: UUID,
    username: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    permission: int = Form(...),
    hub: str = Form(...),
    fk_band: Optional[UUID] = Form(None),
    profile: UploadFile = File(...),
    uow: AbstractUow = Depends(SqlAlchemyUow),
    current_user: User = Depends(
        get_current_user_with_permission(Permissions.student)
    ),
):
    try:
        with uow:
            credentials = Credentials(
                username=username,
                email=email,
                password=password,
            )

            to_update_user = User(
                uuid=uuid,
                credentials=credentials,
                permission=permission,
                hub=hub,
                fk_band=fk_band,
            )

            sv.update_user(uow, to_update_user)
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={
                    'message': 'Usuário atualizado com sucesso.',
                    'data': jsonable_encoder(to_update_user),
                },
            )
    except UserException as error:
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT, content={'message': error.message}
        )
    except SQLAlchemyError:
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={'message': 'Erro interno do servidor.'},
        )


# TODO: Criar o entrypoint para confirmar a criação do usuário
@router.post('/confirm-creation-user')
async def accept_new_user(
    current_user: User = Depends(
        get_current_user_with_permission(Permissions.table)
    ),
):
    ...


# TODO: Deve retornar também o token de acesso do usuário
@router.get('/me/')
async def get_me(
    current_user: User = Depends(
        get_current_user_with_permission(Permissions.student)
    ),
):
    return JSONResponse(
        status_code=HTTPStatus.OK, content=jsonable_encoder(current_user)
    )


def file_iterator(file_path: Path):
    with open(file_path, 'rb') as file:
        while chunk := file.read(1024):  # Lê o arquivo em blocos de 1KB
            yield chunk


@router.get('/profile')
async def get_profile(
    current_user: User = Depends(
        get_current_user_with_permission(Permissions.student)
    ),
):
    try:
        if not current_user.src_profile:
            return Response(status_code=HTTPStatus.NOT_FOUND)
        image = Path(current_user.src_profile)

        if not image.exists() or not image.is_file():
            return Response(status_code=HTTPStatus.NOT_FOUND)
        return StreamingResponse(
            file_iterator(image),
            media_type='image/jpeg',
            status_code=HTTPStatus.OK,
        )

    except Exception as e:
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={'message': 'Erro interno do servidor.'},
        )


@router.post('/activate')
async def activate_users(
    users: list[UUID],
    uow: AbstractUow = Depends(SqlAlchemyUow),
    current_user: User = Depends(
        get_current_user_with_permission(Permissions.table)
    ),
):
    try:
        users_getted = []

        with uow:
            deactivates = sv.get_deactivates(uow)
            for user in users:

                for deactivate in deactivates:
                    if user == deactivate.id:
                        users_getted.append(deactivate)

            if not users_getted:
                return JSONResponse(
                    status_code=HTTPStatus.NOT_FOUND,
                    content={
                        'message': 'Usuários não encontrados',
                        'data': jsonable_encoder(users),
                    },
                )

            sv.activate_users(uow, users_getted)

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={
                    'message': 'Usuários ativados com sucesso.',
                    'data': jsonable_encoder(users),
                },
            )

    except SQLAlchemyError:
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={'message': 'Erro interno do servidor.'},
        )


@router.get('/')
@get_controller(sv)
async def get(
    message_error: str = 'Não foi possível pegar os usuários',
    current_user: User = Depends(
        get_current_user_with_permission(Permissions.table)
    ),
    uow: AbstractUow = Depends(SqlAlchemyUow),
):
    ...


@router.get('/deactivates')
async def get_with_deactivates(
    message_error: str = 'Não foi possível pegar os usuários',
    current_user: User = Depends(
        get_current_user_with_permission(Permissions.table)
    ),
    uow: AbstractUow = Depends(SqlAlchemyUow),
):
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=jsonable_encoder(sv.get_with_deactivates(uow)),
    )


# TODO: Create Delete Method
@router.delete('/{uuid}')
@delete_controller(sv)
async def delete_user(
    uuid: UUID,
    message_success: str = 'Usuário deletado com sucesso.',
    message_error: str = 'Não foi possível deletar o usuário.',
    uow: AbstractUow = Depends(SqlAlchemyUow),
    current_user: User = Depends(
        get_current_user_with_permission(Permissions.table)
    ),
):
    ...
