from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

import error, models, util

from .base_schema import MetaData
from .types_annotated import *
from .user_role_schema import GetUserRole

__all__ = [
    "PostUser",
    "GetUser",
    "PatchUser",
    "ResponseUser",
]


class PostUser(BaseModel):
    """__summary__

    Attributes:
        username (Username): descrever username.
        email (Email): descrever email.
        password (Password): descrever password.
        active (bool): descrever active.
    """

    username: Username = Field(..., description="username Documentar")
    email: Email = Field(..., description="email Documentar")
    password: Password = Field(..., description="password Documentar")
    active: bool | None = Field(None, description="active Documentar")

    @model_validator(mode="before")
    @classmethod
    def validators_user(self, data) -> "PostUser":
        try:
            if not "username" in data:
                raise error.CustomException(
                    422,
                    "É necessário informar o username para prosseguir.",
                )
            if models.User.get("username", data["username"]):
                raise error.CustomException(
                    422,
                    f"'{data['username']}' já está cadastrado.",
                )
            if not "email" in data:
                raise error.CustomException(
                    422,
                    "É necessário informar o email para prosseguir.",
                )
            if models.User.get("email", data["email"]):
                raise error.CustomException(
                    422,
                    f"'{data['email']}' já está cadastrado.",
                )
            pass
            return data
        except Exception as e:
            raise error.custom_HTTPException(e)

class GetUser(BaseModel):
    """__summary__

    Attributes:
        username (Username): descrever username.
        email (Email): descrever email.
        active (bool): descrever active.
        uuid (UUID): descrever uuid.
        created_at (datetime): descrever created_at.
        updated_at (datetime): descrever updated_at.
    """

    username: str = Field(None, description="username Documentar")
    email: str = Field(None, description="email Documentar")
    active: bool | None = Field(None, description="active Documentar")
    uuid: UUID | str = Field(None, description="uuid Documentar")
    created_at: datetime = Field(None, description="created_at Documentar")
    updated_at: datetime | None = Field(
        None, description="updated_at Documentar"
    )
    user_role: list[GetUserRole] | None = None

    model_config = ConfigDict(from_attributes=True)


class PatchUser(BaseModel):
    """__summary__

    Attributes:
        username (Username): descrever username.
        email (Email): descrever email.
        password (Password): descrever password.
        active (bool): descrever active.
    """

    username: Username = Field(None, description="username Documentar")
    email: Email = Field(None, description="email Documentar")
    password: Password = Field(None, description="password Documentar")
    active: bool | None = Field(None, description="active Documentar")


class ResponseUser(BaseModel):
    meta: MetaData
    data: list[GetUser]

    model_config = ConfigDict(from_attributes=True)
