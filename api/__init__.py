from flask import Flask
from flask_restx import Api
from .db import db
from .config.config import config_dict
from .auth.views import namespace as auth_namespace
from .models.students import Student
from flask_jwt_extended import JWTManager


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    
    app.config.from_object(config)
    
    db.init_app(app)
    
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
              title='School Management API',
              description='A basic school management REST API service',
              authorizations=authorizations,
              security='Bearer Auth'
            )
    
    
    
    api.add_namespace(auth_namespace)
    
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'Student': Student,
            # 'Order': Order

        }
    return app
