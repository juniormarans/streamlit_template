from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

import error, models, util

from .base_schema import MetaData
from .types_annotated import *

__all__ = [
    "PostRole",
    "GetRole",
    "PatchRole",
    "ResponseRole",
]


class PostRole(BaseModel):
    """__summary__

    Attributes:
        name (str): descrever name.
        access_level (int): descrever access_level.
        description (str): descrever description.
    """

    name: str = Field(..., description="name Documentar")
    access_level: int = Field(..., description="access_level Documentar")
    description: str | None = Field(None, description="description Documentar")

    @model_validator(mode="before")
    @classmethod
    def validators_role(self, data) -> "PostRole":
        try:
            if not "name" in data:
                raise error.CustomException(
                    422,
                    "É necessário informar o name para prosseguir.",
                )
            if models.Role.get("name", data["name"]):
                raise error.CustomException(
                    422,
                    f"'{data['name']}' já está cadastrado.",
                )
            False
            pass
            return data
        except Exception as e:
            raise error.custom_HTTPException(e)

class GetRole(BaseModel):
    """__summary__

    Attributes:
        name (str): descrever name.
        access_level (int): descrever access_level.
        description (str): descrever description.
        uuid (UUID): descrever uuid.
        created_at (datetime): descrever created_at.
        updated_at (datetime): descrever updated_at.
    """

    uuid: UUID | None = Field(None, description="uuid Documentar")
    name: str | None = Field(None, description="name Documentar")
    access_level: int | None = Field(
        None, description="access_level Documentar"
    )
    description: str | None = Field(None, description="description Documentar")
    created_at: datetime | None = Field(
        None, description="created_at Documentar"
    )
    updated_at: datetime | None = Field(
        None, description="updated_at Documentar"
    )

    model_config = ConfigDict(from_attributes=True)


class PatchRole(BaseModel):
    """__summary__

    Attributes:
        name (str): descrever name.
        access_level (int): descrever access_level.
        description (str): descrever description.
    """

    name: str = Field(None, description="name Documentar")
    access_level: int = Field(None, description="access_level Documentar")
    description: str | None = Field(None, description="description Documentar")


class ResponseRole(BaseModel):
    meta: MetaData
    data: list[GetRole]

    model_config = ConfigDict(from_attributes=True)
