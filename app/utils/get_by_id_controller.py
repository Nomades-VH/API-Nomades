from dataclasses import asdict
from functools import wraps
from http import HTTPStatus
from typing import TypeVar
from uuid import UUID

from fastapi import Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.user.entities import User
from ports.uow import AbstractUow

T = TypeVar("T")


def get_by_id_controller(service):
    def inner(func):
        @wraps(func)
        async def wrapper(
                uuid: UUID,
                message_success: str,
                message_error: str,
                uow: AbstractUow,
                current_user: User
        ) -> Response:
            entity = jsonable_encoder(service.get_by_id(uow, uuid))

            if not entity:
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={"message": message_error}
                )

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content=entity

            )

        return wrapper

    return inner
