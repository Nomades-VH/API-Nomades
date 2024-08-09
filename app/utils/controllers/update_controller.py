from datetime import datetime
from functools import wraps
from http import HTTPStatus
from typing import TypeVar
from uuid import UUID

from sqlalchemy.event import listens_for
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from app.user.entities import User
from ports.uow import AbstractUow
from starlette.responses import Response

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
        ) -> Response:
            response: JSONResponse = await func(uuid, model, message_success, message_error, uow, current_user)
            if response:
                return response

            try:
                with uow:
                    entity = service.get_by_id(uow, uuid)
                    if not entity:
                        return JSONResponse(
                            status_code=HTTPStatus.NOT_FOUND,
                            content={"message": f"{message_error} ID não encontrado."}
                        )

                    if entity == model:
                        print('IGUAIS!!!')
                        return JSONResponse(
                            status_code=HTTPStatus.OK,
                            content={"message": message_success}
                        )
                    print("Não iguais")

                    entity = service.to_update(entity, model, uow)
                    entity.updated_for = current_user.id
                    entity.updated_at = datetime.now()
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
                        "message": f"{e}"
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