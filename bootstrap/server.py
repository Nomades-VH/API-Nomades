from fastapi import FastAPI

from app.band.controllers import router as band_router
from app.breakdown.controllers import router as breakdown_router
from app.kibon_donjak.controllers import router as kibon_donjak_router
from app.kick.controllers import router as kick_router
from app.poomsae.controllers import router as poomsae_router
from app.stretching.controllers import router as stretching_router
from app.theory.controllers import router as theory_router
from app.user.controllers import router as user_router

app = FastAPI(
    title="Band API",
)

app.include_router(router=band_router)
app.include_router(router=breakdown_router)
app.include_router(router=kibon_donjak_router)
app.include_router(router=kick_router)
app.include_router(router=poomsae_router)
app.include_router(router=stretching_router)
app.include_router(router=theory_router)
app.include_router(router=user_router)
