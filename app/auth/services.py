import os
from dataclasses import asdict
from datetime import datetime, timedelta
from typing import Iterator
from uuid import UUID

from aiocron import crontab
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from starlette.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST

from app.auth.exceptions import InvalidCredentials
from app.auth.hasher import verify_password
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

# TODO: Melhorar o tratamento de exceções no código INTEIRO.

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


def get_all(uow: AbstractUow) -> Iterator[Auth]:
    with uow:
        yield from uow.auth.iter()


def auto_revoke_token(uow: AbstractUow = Depends(SqlAlchemyUow)):
    with uow:
        tokens = list(map(asdict, get_all(uow)))

        for token in tokens:
            token = Auth.from_dict(token)
            try:
                if is_revoked_token(uow, token):
                    revoke_token(uow, token.access_token)
            except ExpiredSignatureError as e:
                revoke_token(uow, token.access_token)


@crontab("*/20 * * * *")
async def run_auto_revoke_token():
    uow: AbstractUow = SqlAlchemyUow()
    with uow:
        auto_revoke_token(uow)


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


def invalidate_token(uow: AbstractUow, auth: Auth):
    with uow:
        auth.is_invalid = True
        uow.auth.update(auth)


# TODO: Verificar se realmente está correto
def _is_token_expired(token: Auth):
    try:
        payload = jwt.decode(token.access_token, algorithms=_ALGORITHM, key=_AUTH_SECRET)
        expiration = payload.get('exp')

        if expiration is None:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token inválido")

        return False
    except ExpiredSignatureError:
        return True
    except JWTError:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token inválido")


def is_revoked_token(uow: AbstractUow, token_db: Auth):
    with uow:
        try:
            if not token_db:
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token expirado")

            token_db = uow.auth.get_by_token(token_db.access_token)
            if not token_db:
                return True

            if _is_token_expired(token_db):
                return True

            else:
                return False
        except ExpiredSignatureError:
            return True


async def add_token(uow: AbstractUow, username: str, password: str) -> Auth | str:
    with uow:
        # TODO: Tratamento de erros e exceção
        user = sv.get_user_by_username(uow, username)

        if not user:
            raise InvalidCredentials()

        if not verify_password(password, user.password):
            raise InvalidCredentials()

        token = uow.auth.get_by_user(user.id)

        if not token:
            token = generate_token(username, password, uow)

            uow.auth.add(token)
            return token
        else:
            # TODO: Dessa forma todos os logins terão o mesmo token, se alguem fizer logout, o token será invalidado
            #  em todos os dispositivos.
            if not is_revoked_token(uow, token):
                return token

            token.access_token = _create_token(user.id)

            if token.is_invalid:
                token.is_invalid = False

            uow.auth.update(token)
            return token


def revoke_token(uow: AbstractUow, token: str):
    with uow:
        auth = uow.auth.get_by_token(token)
        if not is_revoked_token(uow, auth):
            auth.is_invalid = True
            uow.auth.update(auth)
        else:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Este token já foi revogado.")


# TODO: Atualizar para o novo modo com o token sendo inserido no banco de dados
def get_current_user(
        uow: AbstractUow = Depends(SqlAlchemyUow), token: str = Depends(oauth2_scheme)
) -> User:
    from app.user.services import get_user_by_id
    with uow:
        try:
            auth = uow.auth.get_by_token(token)

            if is_revoked_token(uow, auth):
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token revogado")

            payload = jwt.decode(auth.access_token, key=_AUTH_SECRET, algorithms=[_ALGORITHM])
            user_id = payload.get("sub")

            if not user_id:
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token inválido")

            user = get_user_by_id(uow, user_id)
            if user is None:
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token inválido")

        except JWTError:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token inválido")

        return user


# TODO: Atualizar para o novo modo com o token sendo inserido no banco de dados
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
