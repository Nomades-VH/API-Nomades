from dataclasses import asdict
from fastapi import APIRouter, Depends, HTTPException
from app.auth.exceptions import InvalidCredentials
from app.auth.schemas import Credentials
from app.uow import SqlAlchemyUow
from ports.uow import AbstractUow
from app.auth.services import generate_token

router = APIRouter(prefix="/auth")


@router.post("")
async def login(credentials: Credentials, uow: AbstractUow = Depends(SqlAlchemyUow)):
    """permissao = Permissions.vice_president.value
    user = User(
        username='admin',
        email='felipesampaio.contato@gmail.com',
        password='admin',
        permission=permissao,
        fk_band=uuid.UUID("bc93a36e-b3e5-49b0-aafe-67283f63aded")
    )

    create_new_user(uow, user)"""
    try:
        token = generate_token(
            email=credentials.email, password=credentials.password, uow=uow
        )

        return asdict(token)
    except InvalidCredentials:
        raise HTTPException(status_code=400, detail="Invalid credentials")
