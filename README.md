# Full Stack Trivia API

Trivia app is a web application that allows users to play trivia and discover who has the most significant knowledge.

## Features

The application has the below functionality:

1. Display questions - either all questions or by a specific category.
2. Delete questions.
3. Add questions.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either by choosing all questions or within a specific category.

## Built with

* React.
* Python.
* Flask Framework.
* Postgres.

## Getting Started

### Installing Dependencies of Backend Part

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

4. **Key Dependencies**

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

---

### Installing Dependencies of Frontend Part

1. **Installing Node and NPM**<br>
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**<br>
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

> _tip_: **npm i** is shorthand for **npm install**

---

### Database Setup

You have two options :
First, With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql myTrivia < trivia.psql
```

Second, You can install `Flask_Migrate` using pip `pip3 install flask_migrate` and then create the migrations using the following commands :
`flask db init`
`flask db migrate`
`flask db upgrade`

then you can run the `seeder.py` file provided to populate the data in the database:
`python3 seeder.py`

Don't forget to change **database_path** in `seeder.py, models.py, and test_flaskr.py` files on the backend folder.

## Run Trivia App

### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

The server will run on [http://localhost:5000](http://localhost:5000).

### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## API Documentation

The application have 7 endpoint which are:

```js
GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
{
    'categories': {
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
```

```js
GET '/questions?page=${integer}'
- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}
```

```js
GET '/categories/${id}/questions'
- Fetches questions for a cateogry specified by id request argument
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
```

```js
DELETE '/questions/${id}'
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.
```

```js
POST '/quizzes'
- Sends a post request in order to get the next question
- Request Body:
{'previous_questions':  an array of question id's such as [1, 4, 20, 15]
'quiz_category': a string of the current category }
- Returns: a single new question object
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer',
        'difficulty': 5,
        'category': 4
    }
}
```

```js
POST '/questions'
- Sends a post request in order to add a new question
- Request Body:
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
- Returns: Does not return any new data
```

```js
POST '/questions'
- Sends a post request in order to search for a specific question by search term
- Request Body:
{
    'searchTerm': 'this is the term the user is looking for'
}
- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'Entertainment'
}
```

## Errors

The Trivia app API uses the following error codes:

| Error Code |        Meaning        |
| ---------- | :-------------------: |
| 400        |      bad request      |
| 404        |  resource not found   |
| 405        |  method not allowed   |
| 422        |     unprocessable     |
| 500        | internal server error |

#### Errors are returned in the following JSON format:

```js
{
'success': False,
'error': 400,
'message': 'bad request'
}
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Authors

Asrar Aljuhani contributed to **add endpoints** and **test cases** in the ****backend part****. I used [@iMishaDev](https://github.com/iMishaDev) [PR](https://github.com/udacity/FSND/pull/134) files.

## Acknowledgments

This project is a part of [Udacity](https://www.udacity.com/) Full Stack Nanodegree and considers one of the projects submitted to graduated from the nanodegree.
