import uuid
from functools import wraps
from http import HTTPStatus
from typing import TypeVar

from fastapi.responses import JSONResponse
from starlette.responses import Response

from app.user.entities import User
from app.utils.Logs import Logs as Log
from ports.uow import AbstractUow

T = TypeVar("T")


def create_controller(service):
    def inner(func):
        @wraps(func)
        @Log.decorators_log(func.__module__, func.__name__)
        async def wrapper(
                model: T,
                message_success: str,
                message_error: str,
                uow: AbstractUow,
                current_user: User
        ) -> Response:
            response: JSONResponse = await func(model, message_success, message_error, uow, current_user)
            if response:
                return response

            try:
                if service.get_by_name(uow, model.name) is not None:
                    return JSONResponse(
                        status_code=HTTPStatus.BAD_REQUEST,
                        content={"message": f"{model.name} já existe."}
                    )

                entity = model.to_create(current_user)
                entity.id = uuid.uuid4()

                service.add(uow, entity)
                return JSONResponse(
                    status_code=HTTPStatus.OK,
                    content={
                        "message": f"{message_success}",
                        "id": str(entity.id)
                    }
                )
            except Exception as e:
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={
                        "message": f"{message_error}"
                    }
                )
        return wrapper
    return inner
