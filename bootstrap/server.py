from http import HTTPStatus
from time import sleep

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from starlette.responses import JSONResponse

from app.auth.controllers import router as auth_router
from app.auth.services import get_current_user
from app.band.controllers import router as band_router
from app.kibon_donjak.controllers import router as kibon_donjak_router
from app.kick.controllers import router as kick_router
from app.poomsae.controllers import router as poomsae_router
from app.uow import SqlAlchemyUow
from app.user.controllers import router as user_router

app = FastAPI(
    title='Nômades',
    # root_path='/nomades'
)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["https://www.nomadesvalehistorico.com.br", "https://nomadesvalehistorico.com.br"],
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    try:
        return JSONResponse(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(
                {
                    'message': f"Argumento inválido ou ausência de argumentos.: {exc.args[0][0]['loc'][1]}"
                }
            ),
        )
    except IndexError:
        return JSONResponse(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(
                {'Message': 'Não foi passado nenhum argumento.'}
            ),
        )


@app.middleware('http')
async def log(request: Request, call_next):
    uow = SqlAlchemyUow()

    try:
        user = get_current_user(
            request.client.host, uow, request.headers['authorization'][7:]
        ).id
    except Exception as e:
        if request.headers.get('authorization'):
            user = request.headers['authorization'][7:]
        else:
            user = None

    response = await call_next(request)
    status = HTTPStatus(response.status_code)

    if 400 <= status <= 499:
        logger.warning(
            f'{request.url} {request.method.upper()}',
            status_code=int(response.status_code),
            user_id=user if user else None,
        )

    elif 500 <= status <= 599:
        logger.critical(
            f'{request.url} {request.method.upper()}',
            status_code=int(response.status_code),
            user_id=user if user else None,
        )

    elif 200 <= status <= 299:
        logger.success(
            f'{request.url} {request.method.upper()}',
            status_code=int(response.status_code),
            user_id=user if user else None,
        )

    elif 300 <= status <= 399:
        logger.debug(
            f'{request.url} {request.method.upper()}',
            status_code=int(response.status_code),
            user_id=user if user else None,
        )

    return response


app.include_router(router=band_router)
app.include_router(router=kibon_donjak_router)
app.include_router(router=kick_router)
app.include_router(router=poomsae_router)
app.include_router(router=user_router)
app.include_router(router=auth_router)
