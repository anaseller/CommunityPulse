from flask import Blueprint, jsonify, request
from src.models.base import Question, Category
from src.dto.poll import QuestionCreate, QuestionResponse
from src.api.decorators.decorators import validate
from src.core.db import db

questions_blueprint = Blueprint('questions', __name__, url_prefix='/api/v1/questions')


@questions_blueprint.route('/', methods=['POST'])
@validate(QuestionCreate)
def create_question(validated_data):

    try:
        category_id = validated_data.category_id
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': f"Category with ID {category_id} not found."}), 404

        new_question = Question(
            title=validated_data.title,
            text=validated_data.text,
            category_id=category_id
        )


        db.session.add(new_question)
        db.session.commit()

        return jsonify(QuestionResponse.from_orm(new_question).dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@questions_blueprint.route('/', methods=['GET'])
def get_questions():

    try:
        questions = Question.query.all()
        questions_response = []
        for q in questions:
            category = Category.query.get(q.category_id)
            if category:
                q_dict = q.to_dict()
                q_dict['category'] = category.to_dict()
                questions_response.append(q_dict)
            else:
                q_dict = q.to_dict()
                q_dict['category'] = None
                questions_response.append(q_dict)

        return jsonify(questions_response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500