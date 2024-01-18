from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from app.band.controllers import router as band_router
from app.breakdown.controllers import router as breakdown_router
from app.kibon_donjak.controllers import router as kibon_donjak_router
from app.kick.controllers import router as kick_router
from app.poomsae.controllers import router as poomsae_router
from app.stretching.controllers import router as stretching_router
from app.theory.controllers import router as theory_router
from app.user.controllers import router as user_router
from app.auth.controllers import router as auth_router

app = FastAPI(
    title="Nômades",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    try:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=jsonable_encoder({
                "message": "Argumento inválido ou ausência de argumentos."
            })
        )
    except IndexError:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=jsonable_encoder({
                "Message": "Não foi passado nenhum argumento."
            })
        )


app.include_router(router=band_router)
app.include_router(router=breakdown_router)
app.include_router(router=kibon_donjak_router)
app.include_router(router=kick_router)
app.include_router(router=poomsae_router)
app.include_router(router=stretching_router)
app.include_router(router=theory_router)
app.include_router(router=user_router)
app.include_router(router=auth_router)
