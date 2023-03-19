from flask import Flask
from flask_restx import Api
from .db import db
from .config.config import config_dict
from .auth.views import namespace as auth_namespace
from .resources.teachers import namespace as teacher_namespace
from .resources.students import namespace as student_namespace
from .resources.courses import namespace as course_namespace
from .resources.grades import namespace as grades_namespace
from .resources.results import namespace as results_namespace
from .models.students import Student
from .models.teachers import Teacher
from .models.courses import Course
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    
    app.config.from_object(config)
    
    db.init_app(app)
    
    migrate = Migrate(app, db)
    
    jwt = JWTManager(app)
    authorizations= {
        "Bearer Auth": {
            'type': 'apiKey',
            'in':'header',
            'name':'Authorization',
            'description': 'Add a JWT token to the header with ** Bearer &lt;JWT&gt; token to authorize **'
        }
    }
    
    api = Api(app,
              title='Student Management API',
              description='A basic school management REST API service',
              authorizations=authorizations,
              security='Bearer Auth'
            )
    
    
    
    api.add_namespace(auth_namespace)
    api.add_namespace(teacher_namespace)
    api.add_namespace(student_namespace)
    api.add_namespace(course_namespace)
    api.add_namespace(grades_namespace)
    api.add_namespace(results_namespace)
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'Student': Student,
            'Teacher': Teacher,
            'Course': Course

        }
    return app
