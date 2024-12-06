import os
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Iterator
from uuid import UUID

from aiocron import crontab
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from starlette.responses import JSONResponse
from starlette.status import HTTP_403_FORBIDDEN

from app.auth.entities import Auth
from app.auth.exceptions import InvalidCredentials
from app.auth.hasher import verify_password
from app.auth.schemas import Credentials
from app.uow import SqlAlchemyUow
from app.user import services as sv
from app.user.entities import User
from general_enum.permissions import Permissions
from ports.uow import AbstractUow

_ALGORITHM = 'HS256'
_TOKEN_EXPIRE_MINUTES = 240
_AUTH_SECRET = os.getenv('AUTH_SECRET')
_SEPARATE_TOKEN = os.getenv('SEPARATE_TOKEN')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth')


# TODO: Melhorar todos os serviços de login, logout, refresh token e auto revoke token
def _create_token(user_id: UUID, ip_user: str) -> str:
    expire = datetime.now() + timedelta(minutes=_TOKEN_EXPIRE_MINUTES)

    return jwt.encode(
        {
            'sub': str(user_id) + _SEPARATE_TOKEN + ip_user,
            'exp': expire,
        },
        key=_AUTH_SECRET,
        algorithm=_ALGORITHM,
    )


def get(uow: AbstractUow) -> Iterator[Auth]:
    with uow:
        yield from uow.auth.iter()


def generate_token(
    user_id, email: str, password: str, uow: AbstractUow, ip_user: str
) -> Auth:
    return Auth(access_token=_create_token(user_id, ip_user), fk_user=user_id)


# É aceitavel que o login demore alguns ms a mais, por conta da segurança
# Esses ms a mais servem para que um ataque de força bruta não funciona corretamente.
async def add(
    uow: AbstractUow, credentials: Credentials, ip_user: str
) -> Auth:
    with uow:
        user = sv.get_user_by_email(
            uow, credentials.email
        ) or sv.get_user_by_username(uow, credentials.username)

        # O ms a mais, vem da verificação de senha
        if not user or not verify_password(
            credentials.password, user.password
        ):
            raise InvalidCredentials('Email ou senha incorretos.')

        token = uow.auth.get_by_user(user.id)

        if token and not is_revoked_token(uow, token):
            payload = jwt.decode(
                token.access_token, key=_AUTH_SECRET, algorithms=[_ALGORITHM]
            )
            ip_user_auth = payload.get('sub').split(_SEPARATE_TOKEN)[1]

            if ip_user_auth != ip_user:
                raise InvalidCredentials()

            return token

        if not token:
            token = generate_token(
                user.id, credentials.email, credentials.password, uow, ip_user
            )
            uow.auth.add(token)
        else:
            token.access_token = _create_token(user.id, ip_user)
            token.is_invalid = False
            uow.auth.update(token)

        return token


def get_current_user(
    ip_user: str,
    uow: AbstractUow = Depends(SqlAlchemyUow),
    token: str = Depends(oauth2_scheme),
) -> User:
    from app.user.services import get_by_id

    with uow:
        try:
            payload = jwt.decode(
                token, key=_AUTH_SECRET, algorithms=[_ALGORITHM]
            )
            user_id = payload.get('sub').split(_SEPARATE_TOKEN)[0]

            if not user_id:
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    detail='Token inválido.',
                )

            auth = uow.auth.get_by_token(token)

            if not auth:
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    detail='Token inválido.',
                )

            ip_user_auth = (
                jwt.decode(
                    auth.access_token,
                    key=_AUTH_SECRET,
                    algorithms=[_ALGORITHM],
                )
                .get('sub')
                .split(_SEPARATE_TOKEN)[1]
            )

            if ip_user_auth != ip_user:
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    detail='Você não tem permissão para acessar essa página.',
                )

            if is_revoked_token(uow, auth):
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    detail='Token revogado.',
                )

            user = get_by_id(uow, user_id)
            if user is None:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail='Usuário não encontrado.',
                )

        except JWTError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail='Token inválido.'
            )

        return user


def get_current_user_with_permission(permission: Permissions):
    def _dependency(
        request: Request,
        uow: AbstractUow = Depends(SqlAlchemyUow),
        auth: str = Depends(oauth2_scheme),
    ) -> User:
        user = get_current_user(request.client.host, uow, auth)

        if user.permission.value < permission.value:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=f'Você não tem autorização para acessar essa página.',
            )

        return user

    return _dependency


@crontab('*/1 * * * *')
async def run_auto_revoke_token():
    uow: AbstractUow = SqlAlchemyUow()
    with uow:
        auto_revoke_token(uow)


def auto_revoke_token(uow: AbstractUow):
    with uow:
        tokens = uow.auth.iter()

        if not tokens:
            return

        for token in tokens:
            try:
                if is_revoked_token(uow, token):
                    invalidate_token(uow, token)
            except ExpiredSignatureError:
                invalidate_token(uow, token)


def revoke_token(uow: AbstractUow, user: User, ip_user):
    with uow:
        auth = uow.auth.get_by_user(user.id)
        if not auth:
            return JSONResponse(
                status_code=HTTPStatus.UNAUTHORIZED,
                content={'message': 'Você não está autenticado.'},
            )

        payload = jwt.decode(
            auth.access_token, key=_AUTH_SECRET, algorithms=[_ALGORITHM]
        )
        ip_user_auth = payload.get('sub').split(_SEPARATE_TOKEN)[1]

        if ip_user_auth != ip_user:
            return InvalidCredentials()

        if not is_revoked_token(uow, auth):
            invalidate_token(uow, auth)
        else:
            invalidate_token(uow, auth)
            return JSONResponse(
                status_code=HTTPStatus.FORBIDDEN,
                content={'message': 'Token anulado.'},
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
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail='Você não está logado'
            )

        payload = jwt.decode(
            token.access_token, algorithms=_ALGORITHM, key=_AUTH_SECRET
        )
        expiration = payload.get('exp')

        if expiration is None:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail='Token inválido'
            )

        timing = expiration - datetime.now().timestamp()

        if timing <= 0:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail='Token expirado'
            )

        return False
    except ExpiredSignatureError:
        return True
    except JWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail='Token inválido'
        )


def invalidate_token(uow: AbstractUow, auth: Auth):
    with uow:
        auth.is_invalid = True
        uow.auth.update(auth)


def refresh_token(
    user: User, token: str, uow: AbstractUow, ip_user: str
) -> Auth:
    with uow:
        auth = uow.auth.get_by_user(user.id)

        if not auth or auth.is_invalid:
            JSONResponse(
                status_code=HTTPStatus.UNAUTHORIZED,
                content={'message': 'Não autenticado.'},
            )

        if not is_revoked_token(uow, auth):
            auth.access_token = _create_token(user.id, ip_user)

            uow.auth.update_from_user(auth, user.id)

            return auth
        else:
            HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail='Token revogado.'
            )
