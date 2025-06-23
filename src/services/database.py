from typing import Any, Type, TypeVar, Optional, List
from sqlalchemy.exc import SQLAlchemyError
# from src.core.db import db
from src.core.app_runner import db
from src.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class DatabaseService:

    @staticmethod
    def create(model: BaseModel) -> tuple[BaseModel, Optional[str]]:
        try:
            db.session.add(model)
            db.session.commit()
            return model, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def get_by_id(model_class: Type[ModelType], model_id: int) -> tuple[Optional[ModelType], Optional[str]]:
        try:
            instance = db.session.query(model_class).get(model_id)
            return instance, None
        except SQLAlchemyError as e:
            return None, str(e)

    @staticmethod
    def get_all(model_class: Type[ModelType]) -> tuple[List[ModelType], Optional[str]]:
        try:
            instances = db.session.query(model_class).all()
            return instances, None
        except SQLAlchemyError as e:
            return [], str(e)

    @staticmethod
    def update(
            model_class: Type[ModelType],
            model_id: int,
            data: dict[str, Any]
    ) -> tuple[Optional[ModelType], Optional[str]]:
        try:
            instance = db.session.query(model_class).get(model_id)
            if not instance:
                return None, f"{model_class.__name__} not found"

            for key, value in data.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)

            db.session.commit()
            return instance, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def delete(model_class: Type[ModelType], model_id: int) -> tuple[bool, Optional[str]]:
        try:
            instance = db.session.query(model_class).get(model_id)
            if not instance:
                return False, f"{model_class.__name__} not found"

            db.session.delete(instance)
            db.session.commit()
            return True, None
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, str(e)