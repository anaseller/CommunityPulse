from flask import jsonify, request
from http import HTTPStatus

from src.services.poll import PollService
from src.core.exceptions import (
    PollNotFoundException,
    PollValidationException,
    PollCreationException,
    PollUpdateException,
    PollDeletionException,
    PollDatabaseException,
    CustomBaseException
)


class PollController:

    def __init__(self):
        self.poll_service = PollService()

    def _handle_poll_exception(self, error: CustomBaseException):
        if isinstance(error, PollNotFoundException):
            return jsonify({
                'status': 'error',
                'message': error.message,
                'code': error.code
            }), HTTPStatus.NOT_FOUND

        elif isinstance(error, PollValidationException):
            return jsonify({
                'status': 'error',
                'message': error.message,
                'code': error.code
            }), HTTPStatus.BAD_REQUEST

        elif isinstance(error, PollCreationException):
            return jsonify({
                'status': 'error',
                'message': error.message,
                'code': error.code
            }), HTTPStatus.BAD_REQUEST

        elif isinstance(error, PollUpdateException):
            return jsonify({
                'status': 'error',
                'message': error.message,
                'code': error.code
            }), HTTPStatus.BAD_REQUEST

        elif isinstance(error, PollDeletionException):
            return jsonify({
                'status': 'error',
                'message': error.message,
                'code': error.code
            }), HTTPStatus.BAD_REQUEST

        elif isinstance(error, PollDatabaseException):
            return jsonify({
                'status': 'error',
                'message': error.message,
                'code': error.code
            }), HTTPStatus.INTERNAL_SERVER_ERROR

        else:
            return jsonify({
                'status': 'error',
                'message': error.message,
                'code': error.code
            }), HTTPStatus.INTERNAL_SERVER_ERROR

    def create_poll(self):
        data = request.get_json()

        if not data:
            error = PollValidationException('No data provided')
            return self._handle_poll_exception(error)

        result = self.poll_service.create_poll(data)

        if isinstance(result, CustomBaseException):
            return self._handle_poll_exception(result)

        return jsonify({
            'status': 'success',
            'message': 'Poll created successfully',
            'data': result
        }), HTTPStatus.CREATED

    def get_polls(self):
        result = self.poll_service.get_all_polls()

        if isinstance(result, CustomBaseException):
            return self._handle_poll_exception(result)

        return jsonify({
            'status': 'success',
            'data': result,
            'count': len(result)
        }), HTTPStatus.OK

    def get_poll(self, poll_id: int):
        result = self.poll_service.get_poll(poll_id)

        if isinstance(result, CustomBaseException):
            return self._handle_poll_exception(result)

        return jsonify({
            'status': 'success',
            'data': result
        }), HTTPStatus.OK

    def update_poll(self, poll_id: int):
        data = request.get_json()

        if not data:
            error = PollValidationException('No data provided')
            return self._handle_poll_exception(error)

        result = self.poll_service.update_poll(poll_id, data)

        if isinstance(result, CustomBaseException):
            return self._handle_poll_exception(result)

        return jsonify({
            'status': 'success',
            'message': 'Poll updated successfully',
            'data': result
        }), HTTPStatus.OK

    def delete_poll(self, poll_id: int):
        result = self.poll_service.delete_poll(poll_id)

        if isinstance(result, CustomBaseException):
            return self._handle_poll_exception(result)

        return jsonify({
            'status': 'success',
            'message': 'Poll deleted successfully'
        }), HTTPStatus.OK