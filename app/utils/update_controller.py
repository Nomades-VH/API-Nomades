from functools import wraps
from http import HTTPStatus
from typing import TypeVar
from uuid import UUID

from loguru import logger
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from app.user.entities import User
from ports.uow import AbstractUow

T = TypeVar("T")


def update_controller(service):
    def inner(func):
        @wraps(func)
        async def wrapper(
                uuid: UUID,
                model: T,
                message_success: str,
                message_error: str,
                uow: AbstractUow,
                current_user: User
        ):
            response = await func(uuid, model, message_success, message_error, uow, current_user)
            if response:
                return response

            entity = service.get_by_id(uow, uuid)
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
            except IntegrityError as e:
                # TODO: IMPORTANTE
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={
                        "message": f"Chave estrangeira inválida"
                    }
                )
            except Exception as e:
                logger.debug(
                    e
                )
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={
                        "message": f"{message_error}",
                        "error": str(e)
                    }
                )
        return wrapper
    return inner