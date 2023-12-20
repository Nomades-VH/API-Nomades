from functools import wraps
from http import HTTPStatus
from uuid import UUID

from fastapi import Response
from fastapi.responses import JSONResponse
from app.user.entities import User
from ports.uow import AbstractUow


def delete_controller(service):
    def inner(func):
        @wraps(func)
        async def wrapper(
                id: UUID,
                message_success: str,
                message_error: str,
                uow: AbstractUow,
                current_user: User
        ) -> Response:
            model = service.get_by_id(uow, id)
            if not model:
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={"message": f"{message_error}"}
                )

            service.delete(uow, model.id)
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={"message": f"{message_success}"}
            )
        return wrapper
    return inner
