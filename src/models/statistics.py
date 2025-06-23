from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.app_runner import db
from src.models.base import BaseModel


class PollStatistics(BaseModel):
    __tablename__ = "poll_statistics"

    poll_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('polls.id'),
        unique=True,
        nullable=False
    )

    total_votes: Mapped[int] = mapped_column(
        db.Integer,
        default=0
    )
    unique_voters: Mapped[int] = mapped_column(
        db.Integer,
        default=0
    )

    # RELATIONS
    poll: Mapped['Poll'] = relationship(
        'Poll',
        back_populates='poll_stats',
    )

    option_stats: Mapped[list['OptionStatistics']] = relationship(
        'OptionStatistics',
        back_populates='statistic',
        cascade='all, delete-orphan',
    )


class OptionStatistics(BaseModel):
    __tablename__ = "option_statistics"

    poll_stats_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('poll_statistics.id'),
        nullable=False
    )

    option_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('poll_options.id'),
        nullable=False
    )

    votes_count: Mapped[int] = mapped_column(
        db.Integer,
        default=0
    )
    percentage: Mapped[float] = mapped_column(
        db.Float,
        default=0.0
    )

    # RELATIONS

    poll_stats: Mapped['PollStatistics'] = relationship(
        'PollStatistics',
        back_populates='option_stats',
    )
    options: Mapped['PollOption'] = relationship(
        'PollOption',
        back_populates='option_stats',
    )