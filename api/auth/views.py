from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.students import Students
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

namespace = Namespace("auth", description="namespace for students authentication")

signup_model = namespace.model(
    "SignUp",
    {
        "name": fields.String(required=True, description="student's name"),
        "email": fields.String(required=True, description="Student's email address"),
        "password": fields.String(required=True, description="Student's Account Password")
    }
)

student_model = namespace.model(
    "Student",
    {
        "id": fields.Integer(),
        "name": fields.String(required=True, description="Student's name"),
        "email": fields.String(required=True, description="Student's email"),
        "password_hash": fields.String(required=True, description="Student's password"),
    }
)

login_model = namespace.model(
    "Login", {
        "email": fields.String(required=True, description="Student's email"),
        "password": fields.String(required=True, description="Student's password"),
    }
)

@namespace.route('/signup')
class Signup(Resource):
    @namespace.expect(signup_model)
    @namespace.marshal_with(student_model)
    def post(self):
        """Sign up a new student
        """
        
        data = namespace.payload
        
        new_student = Students(
            name = data.get("name"),
            email = data.get("email"),
            password_hash = generate_password_hash(data.get("password"))
        )
        
        new_student.save()
        
        return new_student, HTTPStatus.CREATED