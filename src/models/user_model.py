import db
from db.base_class import Base


class User(Base):
    """Modelo da tabela de User

    Attributes:
        username (str): descrever username.
        email (str): descrever username.
        password (bytes): descrever password.
        active (bool): descrever active.
        role_uuid (UUID): descrever role_uuid.
    """

    username: db.Mapped[str] = db.mapped_column(db.String(200))
    email: db.Mapped[str] = db.mapped_column(db.String(100))
    password: db.Mapped[bytes] = db.mapped_column(
        db.LargeBinary, nullable=False
    )
    active: db.Mapped[bool] = db.mapped_column(db.Boolean, default=True)

    # Relationships
    user_role: db.Mapped[list["UserRole"]] = db.relationship(
        "UserRole", back_populates="user", lazy="joined"
    )
