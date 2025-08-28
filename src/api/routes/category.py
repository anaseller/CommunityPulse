from flask import Blueprint, jsonify
from src.models.base import Category

categories_blueprint = Blueprint('categories', __name__)

@categories_blueprint.route('/categories', methods=['GET'])
def get_categories():
    """
    Получает список всех категорий из базы данных
    """
    try:
        categories = Category.query.all()
        return jsonify([c.to_dict() for c in categories]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500