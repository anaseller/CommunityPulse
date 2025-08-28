from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel
from src.core.db import db


class Vote(BaseModel):
    __tablename__ = "votes"

    poll_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('polls.id'),
        nullable=False
    )
    option_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('poll_options.id'),
        nullable=False
    )
    voter_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )
    ip_address: Mapped[str] = mapped_column(
        db.String(56),
        nullable=False
    )
    user_agent: Mapped[str] = mapped_column(
        db.String(150),
        nullable=True
    )

    # RELATIONS

    poll: Mapped["Poll"] = relationship(
        "Poll",
        back_populates="votes"
    )
    option: Mapped["PollOption"] = relationship(
        "PollOption",
        back_populates="votes"
    )
    voter: Mapped["User"] = relationship(
        "User",
        back_populates="votes"
    )