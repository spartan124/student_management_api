
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required)
from flask_restx import Namespace, Resource, abort, fields
from werkzeug.security import check_password_hash, generate_password_hash

from ..models import Admin, Student, Teacher, delete, save, update

namespace = Namespace("auth", description="namespace for Users authentication and Operations")

signup_model = namespace.model(
    "StudentSignUp",
    {
        "name": fields.String(required=True, description="student's name"),
        "email": fields.String(required=True, description="Student's email address"),
        "password": fields.String(required=True, description="Student's Account Password"),
        "role": fields.String(required=True, description="student role")

    }
)

student_model = namespace.model(
    "Student",
    {
        "student_id": fields.Integer(),
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
admin_signup_model = namespace.model( "Admin", {
    "name": fields.String(required=True, description="Admin's name"),
    "email": fields.String(required=True, description="Admin's email"),
    "password": fields.String(required=True, description="Admins's password"),
    "role": fields.String(required=True, description="Admin role")
})
admin_model = namespace.model("AdminModel", {
    "admin_id": fields.Integer(description="Admin ID"),
    "name": fields.String(required=True, description="Admin's name"),
    "email": fields.String(required=True, description="Admin's email"),
    "role": fields.String(required=True, description="Admin role")
})

teacher_signup_model = namespace.model("TeacherX", {
    "name": fields.String(description="Teacher's name"),
    "email": fields.String(description="Teacher's email"),
    "password": fields.String(description="Teacher's password"),
    "role": fields.String(description="Teacher's role")
})
teacher_model = namespace.model("TeacherXY", {
    "teacher_id": fields.Integer(description="Teacher's ID"),
    "name": fields.String(description="Teacher's name"),
    "email": fields.String(description="Teacher's email"),
    "role": fields.String(description="Teacher's role")
})
@namespace.route('/student/signup')
class Signup(Resource):
    @namespace.expect(signup_model)
    @namespace.marshal_with(student_model)
    @namespace.doc(description="Signup a new student account")
    def post(self):
        """Sign up a new student account
        """
        
        data = namespace.payload
        name = data["name"]
        email = data['email']
        password_hash = generate_password_hash(data["password"])
        role = data['role']
        
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

@namespace.route('/admin/signup')
class Signup(Resource):
    @namespace.expect(admin_signup_model)
    @namespace.marshal_with(admin_model)
    @namespace.doc(description="Create a new admin account")
    def post(self):
        """Create a new admin account
        """
        
        data = namespace.payload
        name = data["name"]
        email = data['email']
        password_hash = generate_password_hash(data["password"])
        role = data['role']
        
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

@namespace.route('/teacher/signup')
class Signup(Resource):
    @namespace.expect(teacher_signup_model)
    @namespace.marshal_with(teacher_model)
    @namespace.doc(description="Signup a new Teacher account")
    def post(self):
        """Create a new Teacher account
        """
        
        data = namespace.payload
        name = data["name"]
        email = data['email']
        password_hash = generate_password_hash(data["password"])
        role = data['role']
        
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

