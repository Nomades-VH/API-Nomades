from functools import wraps
from http import HTTPStatus

from starlette.responses import Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.band import services as sv_band
from app.user.entities import User
from general_enum.ModuleType import ModuleType
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

            if current_user.permission.value >= Permissions.table.value:
                entity = jsonable_encoder(service.get(uow))

                if not entity:
                    return JSONResponse(
                        status_code=HTTPStatus.NOT_FOUND,
                        content={"message": message_error},
                    )

                return JSONResponse(
                    status_code=HTTPStatus.OK,
                    content=entity
                )

            func_module_name = func.__module__.split('.')[1]
            if func_module_name in (item.value for item in ModuleType):
                band = sv_band.get_by_user(uow, current_user)

                if band:
                    bands = sv_band.get_minors_band(uow, band.gub)
                    if func_module_name == ModuleType.BAND.value:
                        return JSONResponse(
                            status_code=HTTPStatus.OK,
                            content=jsonable_encoder(bands)
                        )

                    entities = {}
                    for band in bands:
                        if func_module_name == ModuleType.KIBON_DONJAK.value:
                            entities[band.name] = band.kibon_donjaks
                        elif func_module_name == ModuleType.KICK.value:
                            entities[band.name] = band.kicks
                        elif func_module_name == ModuleType.POOMSAE.value:
                            entities[band.name] = band.poomsaes
                else:
                    return JSONResponse(
                        status_code=HTTPStatus.FORBIDDEN,
                        content={"message": "Você não possui uma faixa. Procure mais informações com seu professor."}
                    )

                return JSONResponse(
                    status_code=HTTPStatus.OK,
                    content=jsonable_encoder(entities)
                )

        return wrapper

    return inner
