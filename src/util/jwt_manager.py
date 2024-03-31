from datetime import datetime, timedelta

from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = 'HS256'
JWT_SECRET_KEY = 'secret'


def create_access_token(username: str, expires_delta: int = None) -> str:
    expires_delta = datetime.now(datetime.UTC) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {'exp': expires_delta, 'username': username}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def get_user_from_token(token: str):
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get('username')
