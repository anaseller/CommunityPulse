from typing import List, Union
from sqlalchemy.exc import SQLAlchemyError

from src.core.db import db
from src.models.poll import Poll, PollOption
from src.repositories.base import BaseRepository
from src.core.exceptions import (
    PollCreationException,
)


class PollRepository(BaseRepository):

    def __init__(self):
        super().__init__(Poll)

    def create_with_options(self, poll_data: dict, options_data: List[str]) -> Union[Poll, PollCreationException]:
        try:
            poll = Poll(**poll_data)

            for option_text in options_data:
                option = PollOption(text=option_text)
                poll.options.append(option)

            db.session.add(poll)
            db.session.commit()
            db.session.refresh(poll)

            return poll

        except SQLAlchemyError as e:
            db.session.rollback()
            return PollCreationException(f"Ошибка создания опроса: {str(e)}")