from flask import Flask
from flask_restx import Api
from .db import db
from .config.config import config_dict
from .auth.views import namespace as auth_namespace
from .models.students import Students

def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    
    app.config.from_object(config)
    
    db.init_app(app)
    
    api = Api(app)
    
    
    
    api.add_namespace(auth_namespace)
    
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'Students': Students,
            # 'Order': Order

        }
    return app
