import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_user = "student"
        self.database_passw = "student"
        self.database_name = "trivia_test"
        self.database_path = "postgresql+psycopg2://{}:{}@{}/{}".format(
            self.database_user, self.database_passw,
            'localhost:5432',  self.database_name)
        setup_db(self.app, self.database_path)

        # question dict for testing create new question API
        self.new_question = {
            "question": "Who is Chelsea's most prolific striker?",
            "answer": "Didier Drogba",
            "category": 6,
            "difficulty": 2
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # test for GET categories API
    def test_get_categories(self):
        res = self.client().get('/trivia/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_categories"])
        self.assertTrue(len(data["categories"]))

    # test for GET questions API
    def test_paginated_questions(self):
        res = self.client().get("/trivia/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    # Negative test for getting questions of page that does not exist
    def test_404_get_invalid_page(self):
        res = self.client().get("/trivia/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # test for DELETE question API
    def test_delete_question(self):
        res = self.client().delete("/trivia/questions/2")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)

    # Negative test for deleting question that does not exist
    def test_404_delete_inexistent_question(self):
        res = self.client(). delete('/trivia/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test for creating a new question
    def test_new_question(self):
        res = self.client().post('/trivia/questions', json=self.new_question)
        data = json.loads(res.data)
        pass
    # Negative test for creating new question
    # def test_422_new_question_fails(self):
    #     res = self.client().post('/trivia/questions', json=self.new_question)
    #     data = json.loads(res.data)
    #     pass

    # Test for successful SEARCH question API
    def test_get_search_question(self):
        res = self.client().post('/trivia/questions/search?search=Taj')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 1)

    # Test for SEARCH API using invalid search term
    def test_search_question_no_results(self):
        res = self.client().post('/trivia/questions/search?search=asdfg')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(data['success'], True)

    # Test for fetching questions using category_id
    def test_get_questions_by_category(self):
        res = self.client().get('/trivia/categories/4/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 4)
        self.assertEqual(data['current_category'], 4)

    # Negative Test for getting questions for category_id that does not exist
    def test_404_invalid_category_fetched(self):
        res = self.client().get('/trivia/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['success'], False)

    # Test for playing quiz and fetching random questions
    def test_get_quiz_questions(self):
        quiz = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'sports',
                'id': '6'
            }
        }
        res = self.client().post('/trivia/play', json=quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_quiz_questions(self):
        res = self.client().post('/trivia/play', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
