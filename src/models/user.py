from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel
from src.core.db import db


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        db.String(40),
        unique=True,
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        db.Boolean,
        default=True,
    )
    is_admin: Mapped[bool] = mapped_column(
        db.Boolean,
        default=False,
    )

    # RELATIONS

    votes: Mapped[list['Vote']] = relationship(
        'Vote',
        back_populates='voter',
    )