from flask_restx import Namespace, fields, Resource
from flask import abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.courses import Course


namespace = Namespace('course', description='Course Operations')

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
student_model = namespace.model(
    "Student",
    {
        "student_id": fields.Integer(description="Student ID")
        # "name": fields.String(description="Student name"),
        # "email": fields.String(description="Student's Email"),
        #"courses": fields.String(description="Student's Courses")
    }
)


@namespace.route('/')
class AddGetCourse(Resource):
    @namespace.expect(course_model)
    @namespace.doc(
        description='Add a course to the courses database table'
    )
    @jwt_required()
    def post(self):
        """Add a course 
        """
        data = namespace.payload
        
        course = Course.query.filter_by(course_code=data['course_code']).first()
        
        if course is None:
            course = Course(
                
                course_title = data.get('course_title'),
                course_code = data.get('course_code'),
                description = data.get('description'),
                credit_unit = data.get('credit_unit'),
                teacher_id = data.get('teacher_id'),
            )
            
            course.save()
        
            return {'message': f"Added {data['course_code']} to the database"}, 201
        
        return {'message': f"Course with course code {data['course_code']} already exists in database"}, 409
    
    @namespace.marshal_with(course_model)
    @namespace.doc(description='Get all courses from the database')    
    @jwt_required()
    def get(self):
        """Get all Courses
        """
        courses = Course.query.all()
        return courses, 200
    
@namespace.route('/<int:course_id>')
class GetDeleteUpdateCourse(Resource):
    @namespace.marshal_with(course_model)
    @namespace.doc(
        description='Retrieve a specific course from database by course_id',
        params = {
            "course_id": "ID of the course to retrieve."
        }
    )
    @jwt_required()
    def get(self, course_id):
        """Retrieve a Course

        Args:
            course_id (int): ID of the course to retrieve
        # """
        course = Course.get_by_id(course_id)
        if not course:
            return { "message":"Course {course.course_id} not found."}
        
        return course, 200
    
    @namespace.expect(course_model)
    @namespace.marshal_with(course_model)
    @namespace.doc(
        description='Update a specific course on the database',
        params = {
            "course_id": "ID of the course to update."
        }
    )
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
        return course_to_update, 201
    
    @namespace.marshal_with(course_model)
    @namespace.doc(
        description='Delete a specific course from database.',
        params = {
            "course_id": "ID of the course to delete."
        }
    )
    @jwt_required()
    def delete(self, course_id):
        """Delete a Specific Course

        Args:
            course_id (_int_): Course ID
        """
        course = Course.get_by_id(course_id)
        if course is None:
            return {"message": "Course with {course.course_id} not found"}
        else:
            course.delete()
            return {'message': '{course.course_title} successfully deleted'}, 200

@namespace.route('/<int:course_id>/students')
class EnrolledStudents(Resource):
    @namespace.marshal_with(student_model)
    @namespace.doc(
        description='Retrieve all students enrolled in a course',
        params = {
            "course_id": "ID of the course to retrieve all students."
        }
    )
    def get(self, course_id):
        """Get all students enrolled in a course
        Args:
            course_id (_int_): Course ID
        
        """
        course = Course.get_by_id(course_id)
        if course is None:
            return {"message":"Course with ID {courses.course_id} not found"}, 404
        
        enrolled_students = course.students
             
        
        return enrolled_students, 200
    
  