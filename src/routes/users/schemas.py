from typing import Annotated, Optional

from pydantic import (
    BaseModel,
    EmailStr,
    HttpUrl,
    SecretStr,
    StrictBool,
    StringConstraints,
)


Username = Annotated[str, StringConstraints(max_length=50)]
Email = EmailStr
Bio = str
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
        orm_mode = True

    
    
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


class LoginRequest(BaseModel):
    user: LoginUser


class RegisterUser(BaseRequestUser):
    username: Username


class RegisterRequest(BaseModel):
    user: RegisterUser


class UpdateUser(BaseModel):
    email: Optional[Email]
    username: Optional[Username]
    password: Optional[Password]
    image: Optional[Image]
    bio: Optional[Bio]


class UpdateRequest(BaseModel):
    user: UpdateUser