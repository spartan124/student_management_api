from .courses import Course
from .results import StudentResult
from .students import Student
from .student_course import StudentCourse
from .teachers import Teacher
from .admin import Admin
from ..db import db
from flask_restx import abort
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            current_user = {'role': get_jwt_identity()}
            if current_user['role'] != role:
                abort(403, message='User not Authorized.')
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def save(self):
    db.session.add(self)
    db.session.commit()
    
def update(self):
    db.session.commit()
    
def delete(self):
        db.session.delete(self)
        db.session.commit()
