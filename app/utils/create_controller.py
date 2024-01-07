from functools import wraps
from http import HTTPStatus
from typing import TypeVar

from fastapi.responses import JSONResponse

from app.user.entities import User
from loguru import logger
from ports.uow import AbstractUow

T = TypeVar("T")


def create_controller(service):
    def inner(func):
        @wraps(func)
        async def wrapper(
                model: T,
                message_success: str,
                message_error: str,
                uow: AbstractUow,
                current_user: User
        ):
            response = await func(model, message_success, message_error, uow, current_user)
            if response:
                return response

            try:
                if service.get_by_name(uow, model.name) is not None:
                    logger.info(message_error, extra={
                        'user': current_user.id
                    })
                    return JSONResponse(
                        status_code=HTTPStatus.BAD_REQUEST,
                        content={"message": f"{message_error}: {model.name} já existe."}
                    )

                entity = model.to_entity(current_user)
                service.add(uow, entity)
                return JSONResponse(
                    status_code=HTTPStatus.OK,
                    content={"message": f"{message_success}"}
                )
            except Exception as e:
                logger.warning(message_error, extra={
                    'user': current_user.id,
                    'error': str(e)
                })
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={"message": f"{message_error}"}
                )

        return wrapper

    return inner
