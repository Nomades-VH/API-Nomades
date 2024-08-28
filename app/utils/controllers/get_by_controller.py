from functools import wraps
from http import HTTPStatus
from typing import TypeVar, Any

from starlette.responses import Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.band import services as sv_band
from app.user.entities import User
from general_enum.ModuleType import ModuleType
from general_enum.permissions import Permissions
from ports.uow import AbstractUow

T = TypeVar("T")


def get_by_controller(get_service, entity_name: str):
    def inner(func):
        @wraps(func)
        async def wrapper(
            param: Any, message_error: str, uow: AbstractUow, current_user: User
        ) -> Response:
            response: JSONResponse = await func(param, message_error, uow, current_user)
            if response:
                return response

            if current_user.permission.value >= Permissions.table.value:
                entity = jsonable_encoder(get_service(uow, param))

                if not entity:
                    return JSONResponse(
                        status_code=HTTPStatus.NOT_FOUND,
                        content={"message": message_error},
                    )

                return JSONResponse(status_code=HTTPStatus.OK, content=entity)

            func_module_name = func.__module__.split(".")[1]
            if func_module_name in (item.value for item in ModuleType):
                band = get_service(uow, param)

                if not band:
                    return JSONResponse(
                        status_code=HTTPStatus.FORBIDDEN,
                        content={
                            "message": "Você não tem permissão para encontrar esse recurso."
                        },
                    )

                minors_bands = sv_band.get_minors_band(uow, band.gub)

                if func_module_name == ModuleType.BAND.value:
                    band_by_id = sv_band.get_by_id(uow, param)
                    if band_by_id and band_by_id in minors_bands:
                        return JSONResponse(
                            status_code=HTTPStatus.OK, content=jsonable_encoder(band)
                        )
                    return JSONResponse(
                        status_code=HTTPStatus.FORBIDDEN,
                        content={"message": message_error},
                    )

                for band in minors_bands:
                    for entity in jsonable_encoder(band)[entity_name]:
                        if entity["id"] == str(param):
                            return JSONResponse(
                                status_code=HTTPStatus.OK,
                                content=jsonable_encoder(entity),
                            )

                return JSONResponse(
                    status_code=HTTPStatus.NOT_FOUND,
                    content={"message": message_error},
                )

        return wrapper

    return inner
