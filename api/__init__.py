from flask import Flask
from flask_restx import Api
from .db import db
from .config.config import config_dict

def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    
    app.config.from_object(config)
    
    db.init_app(app)
    
    api = Api(app)
    
    
    
    
    return app
