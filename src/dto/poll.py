from datetime import datetime
from typing import Optional
from pydantic import Field, field_validator, ValidationError

from src.dto.base import (
    BaseDTO,
    IdDTOMixin,
    TimestampDTOMixin
)


class PollOptionRequestDTO(BaseDTO):
    text: str = Field(
        min_length=2,
        max_length=100
    )


class PollRequestDTO(BaseDTO):
    title: str = Field(
        min_length=15,
        max_length=120
    )
    description: Optional[str] = Field(
        default=None,
        max_length=800
    )
    start_date: datetime
    end_date: datetime
    is_active: bool = True
    is_anonymous: bool = True
    options: list[PollOptionRequestDTO] = Field(
        min_length=2
    )

    @field_validator('end_date')
    @classmethod
    def validate_end_date(cls, v, values):
        data: dict = values.data if hasattr(values, 'data') else {}

        start_date = data.get('start_date')  # None as default

        if start_date and v <= start_date:
            raise ValidationError(
                "End date must be greater than start date"
            )

        return v


class PollUpdateRequestDTO(BaseDTO):
    title: Optional[str] = Field(
        None,
        min_length=15,
        max_length=120
    )
    description: Optional[str] = Field(
        default=None,
        max_length=800
    )
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class PollOptionResponseDTO(BaseDTO, IdDTOMixin, TimestampDTOMixin):
    poll_id: int
    text: str


class PollResponseDTO(BaseDTO, IdDTOMixin, TimestampDTOMixin):
    title: str
    description: Optional[str]
    start_date: datetime
    end_date: datetime
    is_active: bool
    is_anonymous: bool
    options: list[PollOptionResponseDTO] = Field(
        default_factory=list
    )


class ShortInfoPollResponseDTO(BaseDTO, IdDTOMixin):
    title: str
    start_date: datetime
    end_date: datetime