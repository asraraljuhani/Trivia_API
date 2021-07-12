import os
from flask import Flask, request, abort, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
from models import setup_db, Question, Category, db
from sqlalchemy.dialects import postgresql

QUESTIONS_PER_PAGE = 10


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def retrieve_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
        except Exception:
            abort(422)

        if len(categories) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'categories': [category.format() for category in categories]
        })

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    @app.route('/questions')
    def retrieve_questions():
        try:
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            categories = Category.query.order_by(Category.id).all()
        except Exception:
            abort(422)

        if len(current_questions) == 0 or len(categories) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': current_questions,
            'totalQuestions': len(Question.query.all()),
            'currentCategory': None,
            'categories': [category.format() for category in categories]
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()

        except Exception:
            if question is None:
                abort(404)
            else:
                abort(500)

        return jsonify({
            'success': True
        })

    @app.route('/questions', methods=['POST'])
    def add_question():
        question_data = request.get_json()['question']
        answer_data = request.get_json()['answer']
        difficulty_data = request.get_json()['difficulty']
        category_data = request.get_json()['category']

        question = Question(question=question_data, answer=answer_data,
                            difficulty=difficulty_data, category=category_data)
        try:
            question.insert()
        except Exception:
            abort(500)

        return jsonify({
            'success': True
        })

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        search_term = request.get_json()['searchTerm']
        try:
            search_results = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
        except Exception:
            abort(500)

        return jsonify({
            'success': True,
            'questions': [question.format() for question in search_results],
            'totalQuestions': len(search_results),
            'currentCategory': None,
        })

    @app.route('/categories/<int:category_id>/questions')
    def retrieve_questions_by_category(category_id):
        try:
            category_id = str(category_id)
            questions = Question.query.order_by(Question.id).filter(
                Question.category == category_id).all()
            categories = Category.query.order_by(Category.id).all()
        except Exception:
            abort(500)
        if len(questions) == 0 or len(categories) == 0 or category_id == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions],
            'totalQuestions': len(Question.query.filter(Question.category == category_id).all()),
            'currentCategory': category_id,
            'categories': [category.format() for category in categories]
        })

    @app.route('/quizzes', methods=['POST'])
    def play_quizze():
        previous_questions = request.get_json()['previous_questions']
        quiz_category_id = request.get_json()['quiz_category'].get('id')

        max_id = db.session.query(func.max(Category.id)).scalar()
        min_id = db.session.query(func.min(Category.id)).scalar()
        # category_id is not exist in the db
        if quiz_category_id > max_id or quiz_category_id < min_id and quiz_category_id != 0:
            abort(404)
        quiz_category_id = str(quiz_category_id)
        # Check if category id equal to zero means all categories; otherwise, a specific category will be.
        try:
            if(quiz_category_id == '0'):
                question = Question.query.filter(~ Question.id.in_(
                    previous_questions)).order_by(func.random()).first()
            else:
                question = Question.query.filter(Question.category == quiz_category_id).filter(
                    ~Question.id.in_(previous_questions)).order_by(func.random()).first()

            # Questions not ended
            if question is not None:
                question = question.format()

        except Exception:
            abort(500)

        return jsonify({
            'success': True,
            'question': question
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app
