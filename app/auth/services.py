import os
from datetime import datetime, timedelta
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.auth.exceptions import InvalidCredentials, InvalidToken
from app.auth.hasher import verify_password
from app.uow import SqlAlchemyUow
from app.user.entities import User
from general_enum.permissions import Permissions
from ports.uow import AbstractUow
from app.auth.value_object import Token

_ALGORITHM = "HS256"
_TOKEN_EXPIRE_MINUTES = 120
_AUTH_SECRET = os.getenv("AUTH_SECRET")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


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


def generate_token(email: str, password: str, uow: AbstractUow) -> Token:
    from app.user.services import get_user_by_email

    user = get_user_by_email(uow, email)
    if not user:
        raise InvalidCredentials()

    if not verify_password(password, user.password):
        raise InvalidCredentials()

    return Token(access_token=_create_token(user.id), refresh_token="")


def get_current_user(
    uow: AbstractUow = Depends(SqlAlchemyUow), auth: str = Depends(oauth2_scheme)
) -> User:
    from app.user.services import get_user_by_id

    try:
        payload = jwt.decode(auth, key=_AUTH_SECRET, algorithms=[_ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_id(uow, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user


def get_current_user_with_permission(permission: Permissions):
    def _dependency(
        uow: AbstractUow = Depends(SqlAlchemyUow), auth: str = Depends(oauth2_scheme)
    ) -> User:
        user = get_current_user(uow, auth)

        if user.permission < permission.value:
            raise HTTPException(
                status_code=401,
                detail=f"You are not authorized to access this resource: expected level permission {permission.value}, but got {Permissions(user.permission).value}",
            )

        return user

    return _dependency
