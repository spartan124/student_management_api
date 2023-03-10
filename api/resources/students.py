from flask_restx import Namespace, fields, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.courses import Course
from ..models.student_course import StudentCourse
from ..models.students import Student

namespace = Namespace('students', description='Student Operations')

student_model = namespace.model(
    "Student",
    {
        "student_id": fields.Integer(description="Student ID"),
        "name": fields.String(description="Student name"),
        "email": fields.String(description="Student's Email"),
        "courses": fields.String(description="Student's Courses")
    }
)
course_model = namespace.model(
    "Course",
    {
        "course_id": fields.Integer(description='Course ID'),
        "course_title": fields.String(description='Course title', required=True),
        "course_code": fields.String(description='Course title', required=True),
        "description": fields.String(description='Course description', required=True),
        "credit_unit": fields.Integer(description='course credit unit', required=True),
        "teacher_id": fields.Integer(description='course teacher ID', required=True),
    }
)
student_course_model = namespace.model(
    "Enrollment",
    {
        "student_id": fields.Integer(description='Student ID'),
        "course_id": fields.Integer(description='Course ID')
    }
    
)
@namespace.route('/')
class GetAllStudents(Resource):
    @namespace.marshal_with(student_model)
    def get(self):
        """_Get all Students_

        Returns:
            _list_: _List of Students_
        """
        students = Student.query.all()
        return students, 200

@namespace.route('/<int:student_id>/course/enroll')    
class EnrollStudentToCourse(Resource):
    @namespace.expect(student_course_model)
    @namespace.marshal_with(student_course_model)
    @jwt_required()
    def post(self, student_id):
        """Enroll a student to a course

        Args:
            student_id (_int_): _Student ID_
        """
        
        data = namespace.payload
        
        student_course = StudentCourse(
            course_id= data['course_id'],
            student_id = data['student_id']
        )
        
        student_course.save()
        return student_course, 201
    
@namespace.route('/<int:student_id>/courses')
class GetEnrolledCourses(Resource):
    @jwt_required()
    @namespace.marshal_with(course_model)
    def get(self, student_id):
        """Get Student's enrolled Courses

        Args:
            student_id (_int_): _Student ID_
        """
        student = Student.get_by_id(student_id)
        courses = student.courses
        
        return courses, 200
    