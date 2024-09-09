from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, APIKeyHeader
from jose import JWTError
from sqlalchemy.orm import Session

from src.routes.users.controller import get_user_by_email
from src.routes.users.models import User as USER

from .db_dependency import get_db
from .jwt_manager import get_email_from_token


class HTTPTokenHeader(APIKeyHeader):
    def __init__(self, raise_error: bool, *args, **kwargs):
        super().__init__(name="Authorization", *args, **kwargs)
        self.raise_error = raise_error

    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        api_key = request.headers.get(self.model.name)
        if not api_key:
            if not self.raise_error:
                return None
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Missing authorization credentials",
            )

        try:
            token_prefix, token = api_key.split(" ")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token schema"
            )

        if token_prefix.lower() != "token":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN_FORBIDDEN,
                detail="Invalid token schema",
            )

        return HTTPAuthorizationCredentials(scheme=token_prefix, credentials=token)


security = HTTPTokenHeader(raise_error=False)


async def get_user_optional(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)] | None,
    db: Session = Depends(get_db),
) -> Optional[USER]:
    if token is None:
        return None
    try:
        email = get_email_from_token(token.credentials)
        user = get_user_by_email(db, email)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not encode token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)] | None,
    db: Session = Depends(get_db),
) -> USER:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await get_user_optional(token, db)  # type: ignore
