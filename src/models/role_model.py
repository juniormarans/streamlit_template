import db
from db.base_class import Base


class Role(Base):
    """Modelo da tabela de Role

    Attributes:
        name (str): nome do papel.
        access_level(int): nivel de permição do papel.
    """

    name: db.Mapped[str] = db.mapped_column(
        db.String(45), nullable=False, unique=True
    )
    access_level: db.Mapped[int] = db.mapped_column(
        db.Integer(), nullable=False
    )
    description: db.Mapped[str | None] = db.mapped_column(db.String(250))

    user_role: db.Mapped[list["UserRole"]] = db.relationship(
        "UserRole", back_populates="role"
    )
