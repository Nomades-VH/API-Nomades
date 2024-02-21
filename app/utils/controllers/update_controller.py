from functools import wraps
from http import HTTPStatus
from typing import TypeVar
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from app.user.entities import User
from app.utils.Logs import Logs as Log
from ports.uow import AbstractUow
from starlette.responses import Response

T = TypeVar("T")


def update_controller(service):
    def inner(func):
        @wraps(func)
        @Log.decorators_log(func.__module__, func.__name__)
        async def wrapper(
                uuid: UUID,
                model: T,
                message_success: str,
                message_error: str,
                uow: AbstractUow,
                current_user: User
        ) -> Response:
            response: JSONResponse = await func(uuid, model, message_success, message_error, uow, current_user)
            if response:
                return response

            entity = service.get_by_id(uow, uuid)
            if not entity:
                return JSONResponse(
                    status_code=HTTPStatus.NOT_FOUND,
                    content={"message": f"{message_error} ID não encontrado."}
                )

            try:
                # TODO: PAdronizar, todos os to_model ficar no entities e todos os to_entity ficar no service.
                entity = service.to_update(entity, model, current_user.id)
                service.update(uow, entity)
                return JSONResponse(
                    status_code=HTTPStatus.OK,
                    content={"message": f"{message_success}"}
                )
            except IntegrityError as e:
                # TODO: IMPORTANTE Usar isso no sistema
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={
                        "message": f"Chave estrangeira inválida"
                    }
                )
            except Exception as e:
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={
                        "message": f"{message_error}",
                        "error": str(e)
                    }
                )
        return wrapper
    return inner