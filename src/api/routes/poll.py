from flask import Blueprint, jsonify, request
from src.models.base import Question, Category
from src.dto.poll import QuestionCreateDTO, QuestionResponseDTO, QuestionUpdateRequestDTO, CategoryResponseDTO
from src.core.db import db
from pydantic import ValidationError

questions_blueprint = Blueprint('questions', __name__, url_prefix='/api/v1/questions')


@questions_blueprint.route('/', methods=['POST'])
def create_question():
    try:
        validated_data = QuestionCreateDTO.model_validate(request.json)

        category = Category.query.get(validated_data.category_id)
        if not category:
            return jsonify({'error': 'Category not found.'}), 404

        new_question = Question(
            title=validated_data.title,
            text=validated_data.text,
            category_id=validated_data.category_id
        )
        db.session.add(new_question)
        db.session.commit()

        response_dto = QuestionResponseDTO.model_validate(new_question)
        if not category:
            response_dto.category = None
        else:
            response_dto.category = CategoryResponseDTO.from_orm(category)

        return jsonify(response_dto.dict()), 201
    except ValidationError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@questions_blueprint.route('/', methods=['GET'])
def get_questions():
    try:
        questions = Question.query.join(Category).all()

        response_dtos = [QuestionResponseDTO.from_orm(q) for q in questions]

        return jsonify([dto.dict() for dto in response_dtos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@questions_blueprint.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    try:
        question = Question.query.join(Category).filter(Question.id == question_id).first_or_404()

        response_dto = QuestionResponseDTO.from_orm(question)

        return jsonify(response_dto.dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@questions_blueprint.route('/<int:question_id>', methods=['PUT', 'PATCH'])
def update_question(question_id):
    try:
        validated_data = QuestionUpdateRequestDTO.model_validate(request.json)

        question = Question.query.get_or_404(question_id)

        for key, value in validated_data.dict(exclude_unset=True).items():
            setattr(question, key, value)

        db.session.commit()

        return jsonify(QuestionResponseDTO.from_orm(question).dict()), 200
    except ValidationError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@questions_blueprint.route('/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    try:
        question = Question.query.get_or_404(question_id)
        db.session.delete(question)
        db.session.commit()
        return jsonify({'message': f'Question with ID {question_id} has been deleted.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500