from uuid import UUID

import db
from db.base_class import Base


class UserRole(Base):
    """Modelo da tabela de Role

    Attributes:
        name (str): nome do papel.
        permission_level(int): nivel de permição do papel.
    """

    user_uuid: db.Mapped[UUID] = db.mapped_column(
        db.UUID(as_uuid=True), db.ForeignKey("user.uuid")
    )
    role_uuid: db.Mapped[UUID] = db.mapped_column(
        db.UUID(as_uuid=True), db.ForeignKey("role.uuid")
    )

    user: db.Mapped["User"] = db.relationship(
        "User", back_populates="user_role"
    )
    role: db.Mapped["Role"] = db.relationship(
        "Role", back_populates="user_role", lazy="joined"
    )
