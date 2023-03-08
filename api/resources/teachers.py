from flask_restx import Namespace, Resource, fields

from ..models.teachers import Teacher

namespace = Namespace('teachers', description='Operations on Teachers')

teacher_model = namespace.model(
    "Teacher",
        {
           "teacher_id": fields.Integer(description="Teacher's ID"),
           "name": fields.String(description="Teacher's name"),
           "email": fields.String(description="Teacher's email"),
        #    "course_id": fields.Integer(description="Course ID")
    }
)

course_model = namespace.model(
    "Courses",
    {
        'course_id': fields.Integer(description='Course ID'),
        'course_title': fields.String(description='Course Title'),
        'course_code': fields.String(description='Course code'),
        'description': fields.String(description='Course Description'),
        'credit_unit': fields.String(description='Course credit unit'),
        'teacher_id': fields.String(descriptiom='Course Teacher ID')
    }
)

@namespace.route('/teacher')
class AddGetTeachers(Resource):
    @namespace.expect(teacher_model)
    @namespace.marshal_with(teacher_model)
    def post(self):
        """Add a Teacher
        """
        data = namespace.payload
        
        add_teacher = Teacher(
            name=data.get('name'),
            email=data.get('email')
        )
        
        add_teacher.save()
        return add_teacher, 201
    
    @namespace.marshal_with(teacher_model) 
    def get(self):
        """Get all Teachers
        """
        
        teachers = Teacher.query.all()
        
        return teachers, 200

@namespace.route('/<int:teacher_id>/courses')
class GetTeacherCourses(Resource):
    
    @namespace.marshal_with(course_model)
    def get(self, teacher_id):
        """Get all Courses by Teacher ID

        Args:
            teacher_id (_int_): _ID of the Teacher_
        """
        teacher = Teacher.get_by_id(teacher_id)
        courses = teacher.courses
        
        return courses, 200
    
    