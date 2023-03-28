
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required)
from flask_restx import Namespace, Resource, abort, fields
from werkzeug.security import check_password_hash, generate_password_hash

from ..models import Admin, Student, Teacher, delete, save, update

namespace = Namespace("auth", description="namespace for Users authentication and Operations")

signup_model = namespace.model(
    "UserSignUp",
    {
        "name": fields.String(required=True, description="student's name"),
        "email": fields.String(required=True, description="Student's email address"),
        "password": fields.String(required=True, description="Student's Account Password"),
        "role": fields.String(required=True, description="student role")

    }
)

user_model = namespace.model(
    "UserModel",
    {
        #"id": fields.Integer(attribute=lambda obj: f"{obj.role}_id"), #if obj.role in ['teacher','student','admin'] else None),
        "name": fields.String(required=True, description="Student's name"),
        "email": fields.String(required=True, description="Student's email"),
        "role": fields.String(required=True, description="student role")
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
    @namespace.marshal_with(user_model)
    @namespace.doc(description="Signup a new student account")
    def post(self):
        """Sign up a new user account
        """
        
        data = namespace.payload
        name = data["name"]
        email = data['email']
        password_hash = generate_password_hash(data["password"])
        role = data['role']
        
        if role == 'teacher':
            
            teacher = Teacher.query.filter_by(email=email).first()
        
            if teacher:
                abort(403, message = "Teacher record already exists")
            else:    
                teacher = Teacher(
                    name = name,
                    email = email,
                    password_hash = password_hash,
                    role = role
                )
                
                save(teacher)
                
                return teacher, 201
            
        elif role == 'student':

            student = Student.query.filter_by(email=email).first()
            
            if student:
                return abort(403, message = "Student record already exists")
            else:    
                new_student = Student(
                    name = name,
                    email = email,
                    password_hash = password_hash,
                    role = role
                )
                
                save(new_student)
                
                return new_student, 201
            
        elif role == 'admin':
            admin = Admin.query.filter_by(email=email).first()
            
            if admin:
                abort(403, message = "Admin record already exists")
            else:    
                admin = Admin(
                    name = name,
                    email = email,
                    password_hash = password_hash,
                    role = role
                )
                
                save(admin)
                
                return admin, 201
        abort (404, "This role does not exist, contact admin")

  
@namespace.route('/login')
class Login(Resource):
    @namespace.expect(login_model)
    @namespace.doc(description="Login a teacher, an admin or a student account and generate access & refresh tokens.")
    def post(self):
        """Generate JWT access and refresh tokens
        """
        
        data = namespace.payload
        
        email = data.get('email')
        password = data.get('password')
        
        admin = Admin.query.filter_by(email=email).first()
        user = Student.query.filter_by(email=email).first()
        teacher = Teacher.query.filter_by(email=email).first()
        
        if (user is not None) and (check_password_hash(user.password_hash, password)):
            access_token = create_access_token(identity=user.email, additional_claims={'role': 'student'})
            refresh_token = create_refresh_token(identity=user.email, additional_claims={'role': 'student'})
            
            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            
            return response, 201
        
        elif (admin is not None) and (check_password_hash(admin.password_hash, password)):
            access_token = create_access_token(identity=admin.email, additional_claims={'role': 'admin'})
            refresh_token = create_refresh_token(identity=admin.email, additional_claims={'role': 'admin'})
            
            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            
            return response, 201
        elif (teacher is not None) and (check_password_hash(teacher.password_hash, password)):
            access_token = create_access_token(identity=teacher.email, additional_claims={'role': 'teacher'})
            refresh_token = create_refresh_token(identity=teacher.email, additional_claims={'role': 'teacher'})
            
            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            
            return response, 201
        
        else:
            abort(403, message="Invalid login credentials. Check credentials and try again.")
        
@namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        email = get_jwt_identity()
        access_token = create_access_token(identity=email)
        response = {
            'access_token':access_token
        }
        return response, 201

