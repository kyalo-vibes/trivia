# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

# API Documentation

## Endpoints

|Method   | API Endpoints                                              | Purpose                                          |                             
|--------------| -------------------------------------------------------|:-------------------------------------------------------:|
|    GET       |```/trivia/categories```                                   |```Fetches a dictionary of categories```                 |      
|    GET      |```/trivia/questions```                                    |```Fetches a dictionary of 10 questions```                             |
|    DELETE    |```/trivia/questions/<int:question_id>```           |```Deletes a particular question```              |
|    POST      |```/trivia/questions```                                    |```Creates a new question```           |
|    POST      |```/trivia/questions/search```                             |```Returns only questions that match the search word```| 
|    GET       |```/trivia/categories/<category_id>/questions```                      |```Fetches a dictionary of questions for a particular category```              |
|    POST      |```/trivia/play```                               |```Starts the quiz and fetches random questions```          | 


### `GET '/trivia/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
- Try: `curl http://127.0.0.1:5000/trivia/categories`

```json
{
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
 "success": true,
  "total_categories": 6
}

```

### `GET '/trivia/questions'`

- Fetches a dictionary of questions in which the keys are the ids and the value is the corresponding string of the question
- Request Arguments: None
- Returns: An object with a single key, `questions`, that contains an object of `id: question_string` key: value pairs limited to only 10 results per page.
- Try: `curl http://127.0.0.1:5000/trivia/questions`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

### `DELETE '/trivia/questions/<int:question_id>'`

- Deletes the question that corresponds to the given question ID. 
- Request Arguments: question_id
- Returns: An object with success message and list of the remaining questions after deletion.
- Try: `curl http://127.0.0.1:5000/trivia/questions/2 -X DELETE`


```json
{
"deleted": 2,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    ],
  "success": true,
  "total_questions": 18
}

```

### `POST '/trivia/questions'`

- Posts a new question into the database with question, answer, category and difficulty fields.
- Request Arguments: None
- Returns: An object with a success message and the list of new questions after insertion.
- Try: `curl http://127.0.0.1:5000/trivia/questions -X POST -H "Content-Type: application/json" -d '{"question": "Who is Chelsea's most prolific striker?", "answer": "Didier Drogba", "category": 6, "difficulty": 2}'`


```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

### `POST '/trivia/questions/search'`

- Searches for questions that match the search word provided.
- Request Arguments: search word
- Returns: A dictionary of questions that matched with the search term.
- Try: `curl http://127.0.0.1:5000/trivia/questions/search?search=Taj -X POST`

```json
{
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

### `GET '/trivia/categories/<category_id>/questions'`

- Fetches a dictionary of questions belonging to the category specified.
- Request Arguments: category_id
- Returns: A dictionary of questions under the given category_id.
- Try: `curl http://127.0.0.1:5000/trivia/categories/1/questions`

```json
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

### `POST '/trivia/play'`

- Starts the quiz by fetching randoming questions for the user to post answers.
- Request Arguments: search word
- Returns: A dictionary of that has not already been used.
- Try: `curl http://127.0.0.1:5000/trivia/play -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": "sports", "id": "6"}}'`

```json
{
  "question": {
    "answer": "Uruguay",
    "category": 6,
    "difficulty": 4,
    "id": 11,
    "question": "Which country won the first ever soccer World Cup in 1930?"
  },
  "success": true
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
