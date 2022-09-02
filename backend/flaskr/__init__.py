from crypt import methods
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# helper function to paginate questions to 10 per page


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS to use trivia as base URL
    CORS(app, resources={r"/trivia/*": {"origins": '*'}})
    # CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, PUT, POST, DELETE, OPTIONS"
        )
        return response

    # origin point of all APIs
    @cross_origin()
    # GET categories API that fetches all categories and orders in ascending
    # order
    @app.route('/trivia/categories', methods=["GET"])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        categories_dict = {
            category.id: category.type for category in categories}

        # raise 404 if categories_dict still has no entry
        if (len(categories_dict) == 0):
            abort(404)

        return jsonify({
            "success": True,
            "categories": categories_dict,
            "total_categories": len(Category.query.all())
        })

    # GET questions API that will only fetch 10 questions per page

    @app.route('/trivia/questions')
    def get_paginated_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        categories = Category.query.all()
        categories_dict = {
            category.id: category.type for category in categories}

        # if no questions are found for page, raise 404 error
        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(Question.query.all()),
            "categories": categories_dict
        })

    # DELETE question API that will delete question of given question_id

    @app.route("/trivia/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        # raise 404 if no question belongs to the given id
        if question is None:
            abort(404)

        question.delete()
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        return jsonify({
            "success": True,
            "deleted": question_id,
            "questions": current_questions,
            "total_questions": len(Question.query.all()),
        })

    # Create question API that will add a new entry to questions table

    @app.route("/trivia/questions", methods=["POST"])
    def create_question():
        body = request.get_json()

        new_question = body.get("question")
        new_answer = body.get("answer")
        new_category = body.get("category")
        new_difficulty = body.get("difficulty")
        search = body.get("search", None)

        try:
            if search:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search))
                )
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    "success": True,
                    "quesitons": current_questions,
                    "total_questions": len(selection.all())
                })

            else:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    category=new_category,
                    difficulty=new_difficulty)
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all())
                })

        # error in case of invalid information provided
        except BaseException:
            abort(422)

    # Search question API that uses ilike to find any question containing the
    # search term
    @app.route("/trivia/questions/search", methods=["POST"])
    def search_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        # body = request.get_json()
        # search = body.get("search")

        search = request.args.get('search', '', type=str)
        search_question = Question.query.filter(
            Question.question.ilike('%{}%'.format(search))).all()
        results = [question.format() for question in search_question]

        # raise 422 if no search term is provided
        if search_question is None:
            abort(422)

        return jsonify({
            'questions': results[start:end],
            'total_questions': len(results),
            'success': True
        })

    # GET questions by category that only fetches questions of a particular
    # category_id
    @app.route('/trivia/categories/<int:category_id>/questions',
               methods=["GET"])
    def get_questions_by_category(category_id):
        category = Category.query.filter_by(id=category_id).one_or_none()

        # raise 404 error if category provided does not exist
        if category is None:
            abort(404)
        try:
            questions = Question.query.filter_by(
                category=str(category_id)).all()
            current_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'total_questions': len(questions),
                'current_category': category_id,
                'questions': current_questions
            })
        # raise 400 error if try does not execute properly
        except BaseException:
            abort(400)

    # Play quiz API for fetching random questions to play quiz
    @app.route('/trivia/play', methods=["POST"])
    def get_quiz_questions():
        try:
            body = request.get_json()
            category = body.get('quiz_category', [])
            previous_questions = body.get('previous_questions', [])

            category_id = category['id']
            next_question = None

            # check if category_id is null
            if category_id != 0:
                # filter questions and fetch only those not in previous
                # questions in specified category
                not_questions = Question.query.filter_by(
                    category=category_id).filter(
                    Question.id.notin_(
                        (previous_questions))).all()
            else:
                # filter questions and fetch only those not in previous
                # questions in any category
                not_questions = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()
            if len(not_questions) > 0:
                next_question = random.choice(not_questions).format()
            return jsonify({
                'success': True,
                'question': next_question
            })

        # raise 422 error if try does not execute properly
        except BaseException:
            abort(422)

    '''
    ERROR HANDLERS
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def request_unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500
    return app
