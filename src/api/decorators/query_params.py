from functools import wraps
from typing import Dict, Type, Union, Any
from dataclasses import dataclass
from flask import request, jsonify
from http import HTTPStatus


@dataclass
class QueryParamSpec:
    """Спецификация query-параметра."""
    type: Type
    required: bool = False
    default: Any = None


def validate_query_params(params_spec: Dict[str, Union[Type, QueryParamSpec]]):
    """
    Декоратор для валидации query-параметров.

    Args:
        params_spec: Спецификация параметров в формате {имя: тип} или {имя: QueryParamSpec}
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Конвертируем простые типы в QueryParamSpec
            full_spec = {
                name: (QueryParamSpec(param_type) if isinstance(param_type, type) else param_type)
                for name, param_type in params_spec.items()
            }

            validated_params = {}
            errors = []

            for param_name, spec in full_spec.items():
                value = request.args.get(param_name)

                # Проверка обязательных параметров
                if value is None:
                    if spec.required:
                        errors.append(f"Missing required query parameter: {param_name}")
                    elif spec.default is not None:
                        validated_params[param_name] = spec.default
                    continue

                # Валидация типа
                try:
                    validated_params[param_name] = _convert_type(value, spec.type)
                except (ValueError, TypeError):
                    errors.append(
                        f"Invalid type for query parameter {param_name}. "
                        f"Expected {spec.type.__name__}, got {value}"
                    )

            if errors:
                return jsonify({
                    'status': 'error',
                    'message': 'Query parameter validation failed',
                    'errors': errors
                }), HTTPStatus.BAD_REQUEST

            # Добавляем валидированные параметры в kwargs
            kwargs.update(validated_params)
            return func(*args, **kwargs)

        return wrapper
    return decorator


def _convert_type(value: Any, target_type: Type) -> Any:
    """
    Преобразует значение к целевому типу.

    Args:
        value: Значение для преобразования
        target_type: Целевой тип

    Returns:
        Any: Преобразованное значение

    Raises:
        ValueError: Если преобразование невозможно
    """
    if isinstance(value, target_type):
        return value

    if target_type is bool:
        if isinstance(value, str):
            value = value.lower()
            if value in ('true', '1', 'yes', 'y', 'on'):
                return True
            if value in ('false', '0', 'no', 'n', 'off'):
                return False
        raise ValueError(f"Cannot convert {value} to bool")

    if target_type in (int, float, str):
        return target_type(value)

    raise ValueError(f"Cannot convert {value} to {target_type}")