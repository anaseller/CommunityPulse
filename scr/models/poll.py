from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseModel
from src.core.app_runner import db


class Poll(BaseModel):
    __tablename__ = "polls"

    title: Mapped[str] = mapped_column(
        db.String(120),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        db.Text,
        nullable=True
    )
    start_date: Mapped[datetime] = mapped_column(
        db.DateTime,
        nullable=False
    )
    end_date: Mapped[datetime] = mapped_column(
        db.DateTime,
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        db.Boolean,
        default=True,
    )
    is_anonymous: Mapped[bool] = mapped_column(
        db.Boolean,
        default=True,
    )