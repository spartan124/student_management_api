from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields, abort

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
        "gpa": fields.Float(description="Student's Grade Point Average")
        
    },
)
course_model = namespace.model(
    "Course",
    {
        "course_id": fields.Integer(description="Course ID"),
        "course_title": fields.String(description="Course title", required=True),
        "course_code": fields.String(description="Course title", required=True),
        "credit_unit": fields.Integer(description="course credit unit", required=True),
        
    },
)
student_course_model = namespace.model(
    "EnrollStudent",
    {
        "student_id": fields.Integer(description="Student ID"),
        "course_id": fields.Integer(description="Course ID"),
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


@namespace.route("/<int:student_id>/course/<int:course_id>/enroll")
class EnrollStudentToCourse(Resource):
    @namespace.expect(student_course_model)
    @namespace.marshal_with(student_course_model)
    @namespace.doc(
        description="Enrolling a student to a course",
        params={
            "student_id": "Id of student to be enrolled in the course",
            "course_id" : "ID of the course to enroll student for"
        }
    )
    @jwt_required()
    def post(self, student_id, course_id):
        """Enroll a student to a course

        Args:
            student_id (_int_): Student ID
            course_id (_int_): Course ID
            
        """
        data = namespace.payload
        
        student_course = StudentCourse.query.filter_by(course_id=course_id, student_id=student_id).first()
        course_id = data.get('course_id')
        student_id = data.get('student_id')
        
        if not student_course:
            student_course = StudentCourse(
                course_id=course_id, 
                student_id=student_id
            )

            student_course.save()
            
            return student_course, 201
        
        abort(403, message="Student already enrolled in course")


@namespace.route("/<int:student_id>/courses")
class GetEnrolledCourses(Resource):
    
    @namespace.marshal_with(course_model)
    @namespace.doc(
        description='Get Student enrolled courses',
        params= {
            'student_id': 'ID of the student'
        }
    )
    @jwt_required()
    def get(self, student_id):
        """Get Student's enrolled Courses

        Args:
            student_id (_int_): _Student ID_
        """
        student = Student.query.filter_by(student_id=student_id).first()
        if student is None:
            abort(404, message="Student not found in database")
            
        courses = student.courses

        return courses, 200


@namespace.route("/<int:student_id>/details")
class StudentDetail(Resource):
    @namespace.marshal_with(student_model)
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
            "email": student.email,
            "courses": student.courses,
            "gpa": student.gpa
        }
        
        return student_data, 200
