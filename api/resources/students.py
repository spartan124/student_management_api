from flask_restx import Namespace, fields, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.courses import Course
from ..models.student_course import StudentCourse
from ..models.students import Student

namespace = Namespace('students', description='Student Operations')

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

@namespace.route('/course')
class AddGetCourse(Resource):
    #@namespace.expect(course_model)
    @namespace.marshal_with(course_model)
    @jwt_required()
    def post(self):
        """Add a course 
        """
        data = namespace.payload
        
        add_course = Course(
            
            course_title = data.get('course_title'),
            course_code = data.get('course_code'),
            description = data.get('description'),
            credit_unit = data.get('credit_unit'),
            teacher_id = data.get('teacher_id'),
        )
        
        add_course.save()
        
        return add_course, 201
    
    @namespace.marshal_with(course_model)    
    @jwt_required()
    def get(self):
        """Retrieves all Courses
        """
        courses = Course.query.all()
        return courses, 200
    
@namespace.route('/course/<int:course_id>')
class GetDeleteUpdateCourse(Resource):
    @namespace.marshal_with(course_model)
    @jwt_required()
    def get(self, course_id):
        """Retrieve a Course

        Args:
            course_id (int): ID of the course to retrieve
        """
        course = Course.get_by_id(course_id)
        return course, 200
    
    @namespace.expect(course_model)
    @namespace.marshal_with(course_model)
    @jwt_required()
    def put(self, course_id):
        """Update a Course

        Args:
            course_id (int): ID of the course to Update
        """
        course_to_update = Course.get_by_id(course_id)
        
        data = namespace.payload
        
        course_to_update.course_title = data['course_title']
        course_to_update.description = data['description']
        course_to_update.credit_unit = data['credit_unit']
        course_to_update.course_code = data['course_code']
        course_to_update.teacher_id = data['teacher_id']
        
        course_to_update.update()
        return course_to_update, 204
    
    @namespace.marshal_with(course_model)
    @jwt_required()
    def get(self, course_id):
        """Delete a Course

        Args:
            course_id (_int_): _Course ID_

        Returns:
            _type_: _description_
        """
        course = Course.get_by_id(course_id)
        course.delete()
        return {'message': '{course.course_title} successfully deleted'}, 200
    
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
    