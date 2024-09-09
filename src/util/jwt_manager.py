import datetime as dt

from jose import jwt

from src.config.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY, ALGORITHM


def create_access_token(email: str, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    expires_delta_dt = dt.datetime.now(dt.UTC) + dt.timedelta(minutes=expires_delta)
    to_encode = {"exp": expires_delta_dt, "context": email}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def get_email_from_token(token: str) -> str:
    payload: dict[str, str] = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get("context", "")
