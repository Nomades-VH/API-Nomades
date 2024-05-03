from functools import wraps
from http import HTTPStatus
from uuid import UUID

from starlette.responses import Response
from fastapi.responses import JSONResponse
from app.user.entities import User
from ports.uow import AbstractUow


def delete_controller(service):
    def inner(func):
        @wraps(func)
        async def wrapper(
                uuid: UUID,
                message_success: str,
                message_error: str,
                uow: AbstractUow,
                current_user: User
        ) -> Response:
            response: JSONResponse = await func(uuid, message_success, message_error, uow, current_user)
            if response:
                return response

            model = service.get_by_id(uow, uuid)
            if not model:
                return JSONResponse(
                    status_code=HTTPStatus.NOT_FOUND,
                    content={"message": f"{message_error}"}
                )

            service.delete(uow, model.id)
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={"message": f"{message_success}"}
            )
        return wrapper
    return inner
