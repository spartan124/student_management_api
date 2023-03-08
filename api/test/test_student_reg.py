import unittest

from werkzeug.security import check_password_hash, generate_password_hash

from .. import create_app
from ..config.config import config_dict
from ..db import db
from ..models.students import Student


class StudentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict["test"])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.client = None

    def test_student_registration(self):
        data = {
            "name": "Test Student",
            "email": "testuser@test.com",
            "password": "password",
        }

        response = self.client.post("/auth/signup", json=data)
        user = Student.query.filter_by(email="testuser@test.com").first()
        assert user.email == "testuser@test.com"
        assert user.name == "Test Student"
        assert response.status_code == 201
    
    def test_student_login(self):
        email = 'testuser@test.com'
        password = 'password'
        password_hash = generate_password_hash(password)
        check_password = check_password_hash(password_hash, password)
        
        data = {
            'email':'testuser@test.com',
            'password': check_password
        }
        
        response = self.client.post('auth/login', json=data)
        
        assert response.status_code == 200