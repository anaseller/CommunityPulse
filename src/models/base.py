from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from typing import Any
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import db


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime,
        default=datetime.now,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False
    )

# Base = declarative_base() class User(Base) -> db.Model
class BaseModel(db.Model, TimestampMixin):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    def to_dict(self) -> dict[str, Any]:
        # [i for i in range(10)]
        # (i for i in range(10))
        # "i for i in range(10)"
        # {i: f"{i*2}" for i in range(10)}
        return {
            col.name: getattr(self, col.name)
            for col in self.__table__.columns
        }


class Category(BaseModel):
    __tablename__ = 'categories'
    name: Mapped[str] = mapped_column(
        db.String(50),
        nullable=False
    )

    questions: Mapped[list['Question']] = relationship(
        back_populates='category'
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
        }


class Question(BaseModel):
    __tablename__ = 'questions'
    title: Mapped[str] = mapped_column(
        db.String(255),
        nullable=False
    )
    text: Mapped[str] = mapped_column(
        db.String(1000),
        nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        db.ForeignKey('categories.id'),
        nullable=False
    )

    category: Mapped['Category'] = relationship(
        back_populates='questions'
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'category_id': self.category_id,
        }