from functools import wraps
from http import HTTPStatus
from typing import Any, TypeVar, Generic

from fastapi.responses import JSONResponse

from app.user.entities import User
from ports.uow import AbstractUow

T = TypeVar("T")


def create_controller(service):
    def inner(func):
        @wraps(func)
        def wrapper(
                entity: T,
                message_success: str,
                message_error: str,
                uow: AbstractUow,
                current_user: User
        ):
            if service.get_by_name(uow, entity.name) is not None:
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={"message": f"{message_error}: {entity.name} já existe."}
                )

            try:
                service.add(uow, entity)
                return JSONResponse(
                    status_code=HTTPStatus.OK,
                    content={"message": f"{message_success}"}
                )
            except Exception as e:
                print(e)
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={"message": f"{message_error}"}
                )
        return wrapper
    return inner
