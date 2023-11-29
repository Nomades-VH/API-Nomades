import json
import os
from datetime import datetime, timedelta
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette.status import HTTP_403_FORBIDDEN

from app.auth.exceptions import InvalidCredentials
from app.auth.hasher import verify_password
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.user import services as sv
from general_enum.permissions import Permissions
from ports.uow import AbstractUow
from app.auth.value_object import Token

# TODO: Ainda há coisas a se fazer. Exemplo: Se o sistema parar e voltar, não terá mais black_list_token, ou seja,
#   os tokens que ainda não passaram do tempo de vencimento, voltarão a ser "válidos"

# TODO: Os métodos fazem as próprias verificações o que resulta em repetição de código,
#  Seria bom já possuir um método que já realizam essas verificações

_ALGORITHM = "HS256"
_TOKEN_EXPIRE_MINUTES = 120
_AUTH_SECRET = os.getenv("AUTH_SECRET")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")
_token_blacklist = set()


def _create_token(user_id: UUID) -> str:
    expire = datetime.utcnow() + timedelta(minutes=_TOKEN_EXPIRE_MINUTES)

    return jwt.encode(
        {
            "sub": str(user_id),
            "exp": expire,
        },
        key=_AUTH_SECRET,
        algorithm=_ALGORITHM,
    )


def generate_token(username: str, password: str, uow: AbstractUow) -> Token:
    from app.user.services import get_user_by_email

    user = sv.get_user_by_username(uow, username)
    if not user:
        raise InvalidCredentials()

    if not verify_password(password, user.password):
        raise InvalidCredentials()

    return Token(access_token=_create_token(user.id))


def refresh_token(user: User, token: str = Depends(oauth2_scheme)) -> Token:
    if not is_revoked_token:
        add_token_blacklist(token)
        return Token(access_token=_create_token(user.id))


def verify_time_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, algorithms=_ALGORITHM, key=_AUTH_SECRET)
        expiration = payload.get('exp')
        if expiration is None:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token expirado")

        timestamp = datetime.utcnow().timestamp() - expiration

        if timestamp <= 0:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token expirado")

        return timestamp
    except JWTError:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token inválido")


def is_revoked_token(token: str = Depends(oauth2_scheme)):
    if verify_time_token(token):
        if token in _token_blacklist:
            return True
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token revogado")


def add_token_blacklist(token: str = Depends(oauth2_scheme)):
    if not is_revoked_token(token):
        _token_blacklist.add(token)
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Esse Token já está revogado.")


def get_current_user(
        uow: AbstractUow = Depends(SqlAlchemyUow), auth: str = Depends(oauth2_scheme)
) -> User:
    from app.user.services import get_user_by_id

    if is_revoked_token(auth):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token revogado")

    try:
        payload = jwt.decode(auth, key=_AUTH_SECRET, algorithms=[_ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token inválido")

        user = get_user_by_id(uow, user_id)
        if user is None:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token inválido")

    except JWTError:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token inválido")

    return user


def get_current_user_with_permission(permission: Permissions):
    def _dependency(
            uow: AbstractUow = Depends(SqlAlchemyUow), auth: str = Depends(oauth2_scheme)
    ) -> User:
        user = get_current_user(uow, auth)

        if user.permission < permission.value:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=f"Você não tem autorização para acessar essa página."
            )

        return user

    return _dependency
