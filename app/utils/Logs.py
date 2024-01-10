import typing
from uuid import UUID

from loguru import logger
from starlette.responses import JSONResponse


class Logs(JSONResponse):
    pass

    @staticmethod
    def decorators_log(module: str, name: str):
        def wrapper(func):
            async def inner(*args, **kwargs):
                response: JSONResponse = await func(*args, **kwargs)
                logger.info(
                    f"{module} {name.upper()}",
                    status_code=int(response.status_code),
                    user_id=str(kwargs['current_user'].id)
                )
                return response

            return inner

        return wrapper



