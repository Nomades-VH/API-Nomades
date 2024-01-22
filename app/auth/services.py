import os
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Iterator
from uuid import UUID

from aiocron import crontab
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from loguru import logger
from starlette.responses import JSONResponse
from starlette.status import HTTP_403_FORBIDDEN

from app.auth.exceptions import InvalidCredentials
from app.auth.hasher import verify_password
from app.auth.schemas import Credentials
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.user import services as sv
from general_enum.permissions import Permissions
from ports.uow import AbstractUow
from app.auth.entities import Auth

_ALGORITHM = "HS256"
_TOKEN_EXPIRE_MINUTES = 120
_AUTH_SECRET = os.getenv("AUTH_SECRET")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


# TODO: Melhorar todos os serviços de login, logout, refresh token e auto revoke token
def _create_token(user_id: UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=_TOKEN_EXPIRE_MINUTES)

    return jwt.encode(
        {
            "sub": str(user_id),
            "exp": expire,
        },
        key=_AUTH_SECRET,
        algorithm=_ALGORITHM,
    )


def get(uow: AbstractUow) -> Iterator[Auth]:
    with uow:
        yield from uow.auth.iter()


def generate_token(username: str, password: str, uow: AbstractUow) -> Auth:
    user = sv.get_user_by_username(uow, username)
    if not user:
        raise InvalidCredentials()

    if not verify_password(password, user.password):
        raise InvalidCredentials()

    return Auth(
        access_token=_create_token(user.id),
        fk_user=user.id
    )


# É aceitavel que o login demore alguns ms a mais, por conta da segurança
# Esses ms a mais servem para que um ataque de força bruta não funciona corretamente.
async def add(uow: AbstractUow, credentials: Credentials) -> Auth:
    with uow:
        user = sv.get_user_by_email(uow, credentials.email) if credentials.email else sv.get_user_by_username(uow,
                                                                                                              credentials.username)
        # O ms a mais, vem da verificação de senha
        if not user or not verify_password(credentials.password, user.password):
            raise InvalidCredentials()

        token = uow.auth.get_by_user(user.id)

        if token and not is_revoked_token(uow, token):
            return token

        if not token:
            token = generate_token(credentials.username, credentials.password, uow)
            uow.auth.add(token)
        else:
            token.access_token = _create_token(user.id)
            token.is_invalid = False
            uow.auth.update(token)

        return token


def get_current_user(
        uow: AbstractUow = Depends(SqlAlchemyUow), token: str = Depends(oauth2_scheme)
) -> User:
    from app.user.services import get_by_id
    with uow:
        try:
            auth = uow.auth.get_by_token(token)

            if is_revoked_token(uow, auth):
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token revogado")

            payload = jwt.decode(auth.access_token, key=_AUTH_SECRET, algorithms=[_ALGORITHM])
            user_id = payload.get("sub")

            if not user_id:
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token inválido")

            user = get_by_id(uow, user_id)
            if user is None:
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Esse usuário não existe")

        except JWTError:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token inválido")

        return user


def get_current_user_with_permission(permission: Permissions):
    def _dependency(
            uow: AbstractUow = Depends(SqlAlchemyUow), auth: str = Depends(oauth2_scheme)
    ) -> User:
        user = get_current_user(uow, auth)

        if user.permission.value < permission.value:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail=f"Você não tem autorização para acessar essa página."
            )

        return user

    return _dependency


@crontab("*/1 * * * *")
async def run_auto_revoke_token():
    uow: AbstractUow = SqlAlchemyUow()
    with uow:
        auto_revoke_token(uow)


def auto_revoke_token(uow: AbstractUow):
    with uow:
        tokens = list(map(asdict, get(uow)))
        if not tokens:
            return

        for token in tokens:
            token = Auth.from_dict(token)
            if token.is_invalid:
                return
            try:
                if is_revoked_token(uow, token):
                    revoke_token(uow, token.access_token)
                    logger.info('Token revogado', extra={'token': token})
            except ExpiredSignatureError as e:
                logger.info('Token revogado', extra={'token': token})
                revoke_token(uow, token.access_token)


def revoke_token(uow: AbstractUow, token: str):
    with uow:
        auth = uow.auth.get_by_token(token)

        if not auth:
            raise HTTPException(
                status_code=403,
                detail={"message": "Você não está logado."}
            )

        if not is_revoked_token(uow, auth):
            invalidate_token(uow, auth)
        else:
            invalidate_token(uow, auth)
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={'message': 'Este token já foi revogado'}
            )


def is_revoked_token(uow: AbstractUow, token_db: Auth):
    with uow:
        try:
            if _is_token_expired(token_db):
                return True
            if token_db.is_invalid:
                return True
            else:
                return False
        except ExpiredSignatureError:
            return True


def _is_token_expired(token: Auth):
    try:
        if not token:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Você não está logado")

        payload = jwt.decode(token.access_token, algorithms=_ALGORITHM, key=_AUTH_SECRET)
        expiration = payload.get('exp')

        if expiration is None:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token inválido")

        return False
    except ExpiredSignatureError:
        return True
    except JWTError:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token inválido")


def invalidate_token(uow: AbstractUow, auth: Auth):
    with uow:
        auth.is_invalid = True
        uow.auth.update(auth)


def refresh_token(user: User, uow: AbstractUow) -> Auth:
    with uow:
        auth = uow.auth.get_by_user(user.id)

        if not auth:
            raise InvalidCredentials()

        if not is_revoked_token(uow, auth):
            auth.access_token = _create_token(user.id)

            uow.auth.update_from_user(auth, user.id)

            return auth
        else:
            HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token revogado.")
