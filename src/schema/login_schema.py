from pydantic import BaseModel, ConfigDict, Field

import core, util

from .base_schema import *
from .user_schema import GetUser

# from .user_schema import GetUser


__all__ = [
    "Login",
    "LoginResponse",
    "ForgotPassword",
    "ForgotPasswordResponse",
    "LoginSessionResponse",
    "ChangePassword",
]


class Login(BaseModel):
    """Schema utilizado no Login

    Attributes:
        username (str): Nome do Usuario.
        password(str): Senha.
    """

    username: str | None = (Field(None, description="username Documentar"),)
    password: str | None = (Field(None, description="password Documentar"),)



class LoginResponse(BaseModel):
    token: str
    user: GetUser

    model_config = ConfigDict(from_attributes=True)


class LoginSessionResponse(BaseModel):
    user: GetUser

    model_config = ConfigDict(from_attributes=True)


class ForgotPassword(BaseModel):
    email: str


class ForgotPasswordResponse(BaseModel):
    token: str

    model_config = ConfigDict(from_attributes=True)


class ChangePassword(BaseModel):
    password: Password
