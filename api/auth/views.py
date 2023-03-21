
from flask_restx import Namespace, Resource, fields, abort
from werkzeug.security import check_password_hash, generate_password_hash
from ..models import Student, Admin, Teacher
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

namespace = Namespace("auth", description="namespace for students authentication")

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
@namespace.route('/signup')
class Signup(Resource):
    @namespace.expect(signup_model)
    @namespace.marshal_with(student_model)
    def post(self):
        """Sign up a new student
        """
        
        data = namespace.payload
        name = data.get("name")
        email = data['email']
        password_hash = generate_password_hash(data.get("password"))
        
        student = Student.query.filter_by(email=email).first()
        
        if student:
            return abort(403, message = "Student record already exists")
        else:    
            new_student = Student(
                name = name,
                email = email,
                password_hash = password_hash
            )
            
            new_student.save()
            
            return new_student, 201

    
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
            
            return response, 201
        
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

@namespace.route('/admin/signup')
class Signup(Resource):
    @namespace.expect(admin_signup_model)
    @namespace.marshal_with(admin_model)
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
            return abort(403, message = "Admin record already exists")
        else:    
            admin = Admin(
                name = name,
                email = email,
                password_hash = password_hash,
                role = role
            )
            
            admin.save()
            
            return admin, 201

    