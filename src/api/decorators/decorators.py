from functools import wraps
from flask import request, jsonify
from pydantic import ValidationError
from http import HTTPStatus


def validate(schema):

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                data = request.get_json()
                validated_data = schema(**data)
                kwargs['validated_data'] = validated_data
                return func(*args, **kwargs)
            except ValidationError as e:
                return jsonify({'error': e.errors()}), HTTPStatus.BAD_REQUEST
            except Exception as e:
                return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST
        return wrapper
    return decorator
