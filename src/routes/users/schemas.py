from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, HttpUrl, SecretStr, StrictBool, StringConstraints

Username = Annotated[str, StringConstraints(max_length=50)]
Email = EmailStr
Bio = str | None
Image = HttpUrl
Following = StrictBool
Password = SecretStr
Token = str


class BaseResponseUser(BaseModel):
    username: Username
    bio: Bio
    image: Image


class AuthenficatedUser(BaseResponseUser):
    email: Email
    token: Token

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: AuthenficatedUser


class Profile(BaseResponseUser):
    following: Following


class ProfileResponse(BaseModel):
    profile: Profile


class BaseRequestUser(BaseModel):
    email: Email
    password: Password


class LoginUser(BaseRequestUser):
    pass


class RegisterUser(BaseRequestUser):
    username: Username


class UpdateUser(BaseModel):
    email: Optional[Email] = None
    username: Optional[Username] = None
    password: Optional[Password] = None
    image: Optional[Image] = None
    bio: Optional[Bio] = None
