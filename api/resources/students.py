from flask import abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from ..models.courses import Course
from ..models.student_course import StudentCourse
from ..models.students import Student

namespace = Namespace("students", description="Student Operations")

student_model = namespace.model(
    "Student",
    {
        "student_id": fields.Integer(description="Student ID"),
        "name": fields.String(description="Student name"),
        "email": fields.String(description="Student's Email"),
        "courses": fields.String(description="Student's Courses"),
        
    },
)
course_model = namespace.model(
    "Course",
    {
        "course_id": fields.Integer(description="Course ID"),
        "course_title": fields.String(description="Course title", required=True),
        "course_code": fields.String(description="Course title", required=True),
        # "description": fields.String(description="Course description", required=True),
        "credit_unit": fields.Integer(description="course credit unit", required=True),
        # "teacher_id": fields.Integer(description="course teacher ID", required=True),
    },
)
student_course_model = namespace.model(
    "Enrollment",
    {
        "student_id": fields.Integer(description="Student ID"),
        "course_id": fields.Integer(description="Course ID"),
        "credit_unit": fields.Integer(description="course credit unit", required=True),
    },
)
results_model =namespace.model(
    "Results",
    {
        "course_id": fields.Integer(description="Course ID"),
        "course_code": fields.String(description="Course title", required=True),
        "course_title": fields.String(description="Course title", required=True),
        "credit_unit": fields.Integer(description="course credit unit", required=True),
        'grade': fields.String(description='Grade in Course'),
        'earned_credit_unit': fields.String(description='Credit unit earned'),
        
    }
)

@namespace.route("/")
class GetAllStudents(Resource):
    @namespace.marshal_with(student_model)
    def get(self):
        """Get all Students

        Returns:
            _list_: List of Students
        """
        students = Student.query.all()
        return students, 200


@namespace.route("/<int:student_id>/course")
class EnrollStudentToCourse(Resource):
    @namespace.expect(student_course_model)
    @namespace.marshal_with(student_course_model)
    @namespace.doc(
        description="Enrolling a student to a course",
        params={
            # "course_id": "ID of the course to enroll",
            "student_id": "Id of student to be enrolled in the course",
        },
    )
    # @jwt_required()
    def post(self, student_id):
        """Enroll a student to a course

        Args:
            student_id (_int_): Student ID
        """

        data = namespace.payload

        student_course = StudentCourse(
            course_id=data["course_id"], student_id=student_id
        )

        student_course.save()
        return student_course, 201


@namespace.route("/<int:student_id>/courses")
class GetEnrolledCourses(Resource):
    
    @namespace.marshal_with(course_model)
    @namespace.doc(
        description='Get Student enrolled courses',
        params= {
            'student_id': 'ID of the student'
        }
    )
    # @jwt_required()
    def get(self, student_id):
        """Get Student's enrolled Courses

        Args:
            student_id (_int_): _Student ID_
        """
        student = Student.get_by_id(student_id)
        courses = student.courses

        return courses, 200


@namespace.route("/<int:student_id>/details")
class StudentDetail(Resource):
    @namespace.marshal_with(results_model)
    @namespace.doc(
        description='Get Student detail',
        params= {
            'student_id': 'ID of the student'
        }
    )
    def get(self, student_id):
        student = Student.get_by_id(student_id)
        if not student:
            abort(404, f"Student {student_id} not found")
        student_data = {
            "student_id": student.student_id,
            "name": student.name,
            "courses": student.courses,
            "gpa": student.gpa
        }
        
        return student_data, 200
