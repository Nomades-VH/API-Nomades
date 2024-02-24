from functools import wraps
from http import HTTPStatus
from typing import List

from starlette.responses import Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.band import services as sv_band
from app.user.entities import User
from general_enum.permissions import Permissions
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

            possibilities: List[str] = ['band', 'kibon_donjak', 'kick', 'poomsae']
            func_module_name = func.__module__.split('.')[1]
            if func_module_name in possibilities and is_student(user=current_user):
                band = sv_band.get_by_user(uow, current_user)

                if band:
                    bands = sv_band.get_minors_band(uow, band.gub)
                    if func_module_name == possibilities[0]:
                        return JSONResponse(
                            status_code=HTTPStatus.OK,
                            content=jsonable_encoder(bands)
                        )

                    entities = {}
                    for band in bands:
                        if func_module_name == possibilities[1]:
                            entities[band.name] = band.kibon_donjaks
                        elif func_module_name == possibilities[2]:
                            entities[band.name] = band.kicks
                        elif func_module_name == possibilities[3]:
                            entities[band.name] = band.poomsaes

                return JSONResponse(
                    status_code=HTTPStatus.FORBIDDEN,
                    content={"message": "Você não possui uma faixa. Procure mais informações com seu professor."}
                )
            else:
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


def is_student(user: User) -> bool:
    return user.permission == Permissions.student
