from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel
from src.core.db import db


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

    # Relations

    options: Mapped[list["PollOption"]] = relationship(
        "PollOption",
        back_populates="poll",
        cascade="all, delete-orphan"
    )
    votes: Mapped[list["Vote"]] = relationship(
        "Vote",
        back_populates="poll",
        cascade="all, delete-orphan"
    )
    statistics: Mapped["PollStatistics"] = relationship(
        "PollStatistics",
        back_populates="poll",
        uselist=False,  # One-to-One отношение
        cascade="all, delete-orphan"
    )


class PollOption(BaseModel):
    __tablename__ = "poll_options"

    poll_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('polls.id'),
        nullable=False
    )
    text: Mapped[str] = mapped_column(
        db.String(80),
        nullable=False
    )

    # Relations

    poll: Mapped["Poll"] = relationship(
        "Poll",
        back_populates="options"
    )
    votes: Mapped[list["Vote"]] = relationship(
        "Vote",
        back_populates="option"
    )
    option_stats: Mapped["OptionStatistics"] = relationship(
        "OptionStatistics",
        back_populates="option",
    )