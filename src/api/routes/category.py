from flask import Blueprint, jsonify, request
from src.models.base import Category
from src.dto.poll import CategoryRequestDTO, CategoryResponseDTO
from src.api.decorators.decorators import validate
from src.core.db import db
from pydantic import ValidationError

categories_blueprint = Blueprint('categories', __name__, url_prefix='/api/v1/categories')


@categories_blueprint.route('/', methods=['POST'])
def create_category():

    try:
        validated_data = CategoryRequestDTO.model_validate(request.json)

        new_category = Category(name=validated_data.name)
        db.session.add(new_category)
        db.session.commit()
        return jsonify(CategoryResponseDTO.from_orm(new_category).dict()), 201
    except ValidationError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@categories_blueprint.route('/', methods=['GET'])
def get_categories():

    try:
        categories = Category.query.all()
        return jsonify([CategoryResponseDTO.from_orm(c).dict() for c in categories]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@categories_blueprint.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):

    try:

        validated_data = CategoryRequestDTO.model_validate(request.json)

        category = Category.query.get_or_404(category_id)
        category.name = validated_data.name
        db.session.commit()
        return jsonify(CategoryResponseDTO.from_orm(category).dict()), 200
    except ValidationError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@categories_blueprint.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):

    try:
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': f'Category with ID {category_id} has been deleted.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500