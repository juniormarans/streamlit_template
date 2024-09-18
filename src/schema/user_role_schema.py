from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

import error, models, util

from .base_schema import MetaData
from .types_annotated import *

# from .role_schema import GetRole


__all__ = [
    "PostUserRole",
    "GetUserRole",
    "PatchUserRole",
    "ResponseUserRole",
]


class PostUserRole(BaseModel):
    """__summary__

    Attributes:
        user_uuid (UUID): descrever user_uuid.
        role_uuid (UUID): descrever role_uuid.
    """

    user_uuid: UUID | None = Field(None, description="user_uuid Documentar")
    role_uuid: UUID | None = Field(None, description="role_uuid Documentar")

    @model_validator(mode="before")
    @classmethod
    def validators_user_role(self, data) -> "PostUserRole":
        try:
            False
            pass
            return data
        except Exception as e:
            raise error.custom_HTTPException(e)

class GetUserRole(BaseModel):
    """__summary__

    Attributes:
        user_uuid (UUID): descrever user_uuid.
        role_uuid (UUID): descrever role_uuid.
        uuid (UUID): descrever uuid.
        created_at (datetime): descrever created_at.
        updated_at (datetime): descrever updated_at.
    """

    user_uuid: UUID | None = Field(None, description="user_uuid Documentar")
    role_uuid: UUID | None = Field(None, description="role_uuid Documentar")
    uuid: UUID | None = Field(None, description="uuid Documentar")
    created_at: datetime | None = Field(
        None, description="created_at Documentar"
    )
    updated_at: datetime | None = Field(
        None, description="updated_at Documentar"
    )
    #    role: list[GetRole | None]

    model_config = ConfigDict(from_attributes=True)


class PatchUserRole(BaseModel):
    """__summary__

    Attributes:
        user_uuid (UUID): descrever user_uuid.
        role_uuid (UUID): descrever role_uuid.
    """

    user_uuid: UUID | None = Field(None, description="user_uuid Documentar")
    role_uuid: UUID | None = Field(None, description="role_uuid Documentar")


class ResponseUserRole(BaseModel):
    meta: MetaData
    data: list[GetUserRole]

    model_config = ConfigDict(from_attributes=True)
