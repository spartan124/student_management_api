Student Management API

This is a Flask app that provides an API for managing courses, students, and teachers, and their relationships, such as student enrollments and grades. It includes a SQLite database to store data.

Project Tree
The project tree is organized as follows:

```markdown
.
├── Procfile
├── README.md
├── api
│   ├── __init__.py
│   ├── auth
│   │   └── views.py
│   ├── config
│   │   ├── config.py
│   │   ├── db.sqlite3
│   │   └── db1.sqlite3
│   ├── db.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── courses.py
│   │   ├── results.py
│   │   ├── student_course.py
│   │   ├── students.py
│   │   └── teachers.py
│   ├── resources
│   │   ├── courses.py
│   │   ├── grades.py
│   │   ├── results.py
│   │   ├── students.py
│   │   └── teachers.py
│   └── test
│       ├── __init__.py
│       ├── test_courses.py
│       ├── test_grades.py
│       ├── test_students.py
│       └── test_teachers.py
├── proj_tree.txt
├── project_tree.sh
├── project_tree.txt
├── requirements.txt
└── server.py
```
Procfile: A configuration file for Heroku deployment.
README.md: This file.
api: The main package of the app, containing the source code.
api/__init__.py: Initializes the Flask app and sets up the database.
api/auth/views.py: Defines authentication views for the app.
api/config: Contains configuration files and the SQLite databases.
api/db.py: Defines a SQLAlchemy database object.
api/models: Defines the database models for courses, students, teachers, student enrollments, and grades.
api/resources: Defines the Flask-RESTful resources for CRUD operations on courses, students, teachers, student enrollments, and grades.
api/test: Contains unit tests for the app.
project_tree.sh: A shell script that generates project_tree.txt.
project_tree.txt: A text file listing the project tree.
requirements.txt: A list of Python dependencies for the app.
server.py: Runs the Flask app.

Usage
To run the app locally, you need to have Python and pip installed. Then, follow these steps:

    1.  Clone the repository:
        ```bash
        git clone <repository-url>
        cd <repository-name>
        ```
    2.  Create a virtual environment and activate it:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    