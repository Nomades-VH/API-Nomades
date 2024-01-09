from functools import wraps
from http import HTTPStatus
from typing import TypeVar, Any

from fastapi import Depends
from loguru import logger
from starlette.responses import Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.auth.services import get_current_user_with_permission
from app.user.entities import User
from general_enum.permissions import Permissions
from ports.uow import AbstractUow

T = TypeVar("T")


def get_by_controller(get_service):
    def inner(func):
        @wraps(func)
        async def wrapper(
                param: Any,
                message_success: str,
                message_error: str,
                uow: AbstractUow,
                current_user: User
        ) -> Response:
            print(current_user)
            response = await func(param, message_success, message_error, uow, current_user)
            if response:
                return response

            entity = jsonable_encoder(get_service(uow, param))

            if not entity:
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={"message": message_error + f' Identificador {param} não encontrado.'}
                )

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content=entity
            )

        return wrapper

    return inner
