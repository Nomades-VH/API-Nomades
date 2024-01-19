from functools import wraps
from http import HTTPStatus
from typing import TypeVar, Any

from starlette.responses import Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.user.entities import User
from app.utils.Logs import Logs as Log
from ports.uow import AbstractUow

T = TypeVar("T")


def get_by_controller(get_service):
    def inner(func):
        @wraps(func)
        @Log.decorators_log(func.__module__, func.__name__)
        async def wrapper(
                param: Any,
                message_error: str,
                uow: AbstractUow,
                current_user: User
        ) -> Response:
            response: JSONResponse = await func(param, message_error, uow, current_user)
            if response:
                return response

            entity = jsonable_encoder(get_service(uow, param))

            if not entity:
                response = JSONResponse(
                    status_code=HTTPStatus.NOT_FOUND,
                    content={"message": message_error},
                )
                return response

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content=entity
            )

        return wrapper
    return inner
