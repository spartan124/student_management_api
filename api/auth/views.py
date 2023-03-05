from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.students import Student
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
        
        new_student = Student(
            name = data.get("name"),
            email = data.get("email"),
            password_hash = generate_password_hash(data.get("password"))
        )
        
        new_student.save()
        
        return new_student, HTTPStatus.CREATED
    
@namespace.route('/login')
class Login(Resource):
    @namespace.expect(login_model)
    def post(self):
        """Generate JWT access and refresh tokens
        """
        
        data = namespace.payload
        
        email = data.get('email')
        password = data.get('password')
        
        user = Student.query.filter_by(email=email).first()
        
        if (user is not None) and (check_password_hash(user.password_hash, password)):
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)
            
            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            
            return response, HTTPStatus.CREATED
        
@namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        email = get_jwt_identity()
        access_token = create_access_token(identity=email)
        response = {
            'access_token':access_token
        }
        return response, HTTPStatus.CREATED
    