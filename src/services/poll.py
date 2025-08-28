from typing import List, Dict, Any, Union

from src.repositories.poll import PollRepository

from src.dto import (
    PollRequestDTO,
    PollUpdateRequestDTO,
    PollResponseDTO,
    ShortInfoPollResponseDTO
)
from src.core.exceptions import (
    CustomBaseException,
    EntityNotFoundException,
    DatabaseException,
    PollNotFoundException,
    PollValidationException,
    PollCreationException,
    PollUpdateException,
    PollDeletionException,
    PollDatabaseException
)


class PollService:

    def __init__(self):
        self.poll_repository = PollRepository()

    def create_poll(self, data: Dict[str, Any]) -> Union[Dict, CustomBaseException]:
        try:
            poll_dto = PollRequestDTO(**data)

            poll_data = {
                'title': poll_dto.title,
                'description': poll_dto.description,
                'start_date': poll_dto.start_date,
                'end_date': poll_dto.end_date,
                'is_anonymous': poll_dto.is_anonymous,
                'is_active': poll_dto.is_active
            }

            options_texts = [option.text for option in poll_dto.options]

            result = self.poll_repository.create_with_options(poll_data, options_texts)

            if isinstance(result, PollCreationException):
                return result

            poll_response = PollResponseDTO.model_validate(result)

            return poll_response.model_dump(mode='json')

        except Exception as e:
            return PollValidationException(f"Ошибка валидации: {str(e)}")

    def get_poll(self, poll_id: int) -> Union[Dict, CustomBaseException]:
        result = self.poll_repository.get_by_id(poll_id)

        # Обрабатываем все возможные типы исключений из репозитория
        if isinstance(result, EntityNotFoundException):
            return PollNotFoundException(result.message)

        if isinstance(result, DatabaseException):
            return PollDatabaseException(result.message)

        if isinstance(result, (PollNotFoundException, PollDatabaseException)):
            return result

        poll_response = PollResponseDTO.model_validate(result)

        return poll_response.model_dump(mode='json')

    def get_all_polls(self) -> Union[List[Dict], PollDatabaseException]:
        result = self.poll_repository.get_all()

        if isinstance(result, DatabaseException):
            return PollDatabaseException(result.message)

        if isinstance(result, PollDatabaseException):
            return result

        polls_list = [ShortInfoPollResponseDTO.model_validate(poll).model_dump(mode='json')
                      for poll in result]

        return polls_list

    def update_poll(self, poll_id: int, data: Dict[str, Any]) -> Union[Dict, CustomBaseException]:
        try:
            poll_dto = PollUpdateRequestDTO(**data)

            update_data = poll_dto.model_dump(exclude_unset=True, exclude_none=True)

            if not update_data:
                return PollValidationException("Нет данных для обновления")

            result = self.poll_repository.update(poll_id, update_data)

            # Обрабатываем все возможные типы исключений из репозитория
            if isinstance(result, EntityNotFoundException):
                return PollNotFoundException(result.message)

            if isinstance(result, DatabaseException):
                return PollDatabaseException(result.message)

            if isinstance(result, (PollNotFoundException, PollUpdateException)):
                return result

            poll_response = PollResponseDTO.model_validate(result)

            return poll_response.model_dump(mode='json')

        except Exception as e:
            return PollValidationException(f"Ошибка валидации: {str(e)}")

    def delete_poll(self, poll_id: int) -> Union[bool, CustomBaseException]:
        result = self.poll_repository.delete(poll_id)

        # Обрабатываем все возможные типы исключений из репозитория
        if isinstance(result, EntityNotFoundException):
            return PollNotFoundException(result.message)

        if isinstance(result, DatabaseException):
            return PollDeletionException(result.message)

        if isinstance(result, (PollNotFoundException, PollDeletionException)):
            return result

        return result