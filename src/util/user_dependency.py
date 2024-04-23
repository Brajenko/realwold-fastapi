from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from src.routes.users.controller import get_user_by_email
from src.routes.users.models import User as USER

from .db_dependency import get_db
from .jwt_manager import get_email_from_token


security = HTTPBearer(auto_error=False)


async def get_user_optional(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(get_db),
) -> USER:
    if token is None:
        return None
    try:
        email = get_email_from_token(token.credentials)
        user = get_user_by_email(db, email)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not encode token',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user


async def get_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(get_db),
) -> USER:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return await get_user_optional(token, db)
