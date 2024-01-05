from functools import wraps
from http import HTTPStatus
from typing import TypeVar
from uuid import UUID

from starlette.responses import JSONResponse

from app.user.entities import User
from ports.uow import AbstractUow

T = TypeVar("T")


def update_controller(service):
    def inner(func):
        @wraps(func)
        def wrapper(
                id: UUID,
                model: T,
                message_success: str,
                message_error: str,
                uow: AbstractUow,
                current_user: User
        ):
            entity = service.get_by_id(uow, id)
            if not entity:
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={"message": f"{message_error}"}
                )

            try:
                entity = service.to_entity(entity, model)
                service.update(uow, entity)
                return JSONResponse(
                    status_code=HTTPStatus.OK,
                    content={"message": f"{message_success}"}
                )
            except Exception as e:
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={"message": f"{message_error}"}
                )
        return wrapper
    return inner