from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException

from app.auth.exceptions import InvalidCredentials
from app.auth.schemas import Credentials
from app.uow import SqlAlchemyUow
from ports.uow import AbstractUow
from app.auth.services import generate_token

router = APIRouter(prefix="/auth")


# TODO: A API ainda permite o acesso as urls mesmo sem estar logado

@router.post("")
async def login(credentials: Credentials, uow: AbstractUow = Depends(SqlAlchemyUow)):
    try:
        token = generate_token(
            email=credentials.username,
            password=credentials.password,
            uow=uow
        )

        return asdict(token)
    except InvalidCredentials:
        raise HTTPException(status_code=400, detail="Invalid credentials")
