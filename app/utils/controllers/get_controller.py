from functools import wraps
from http import HTTPStatus

from starlette.responses import Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.user.entities import User
from ports.uow import AbstractUow
from app.utils.Logs import Logs as Log


def get_controller(service):
    def inner(func):
        @wraps(func)
        @Log.decorators_log(func.__module__, func.__name__)
        async def wrapper(
                message_error: str,
                current_user: User,
                uow: AbstractUow
        ) -> Response:
            response: JSONResponse = await func(message_error, current_user, uow)
            if response:
                return response

            entities = jsonable_encoder(service.get(uow))

            if entities:
                return JSONResponse(
                    status_code=HTTPStatus.OK,
                    content=entities
                )

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={
                    "message": message_error
                }
            )

        return wrapper

    return inner
