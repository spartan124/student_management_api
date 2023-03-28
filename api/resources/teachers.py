from flask_restx import Namespace, Resource, abort, fields
from flask_jwt_extended import jwt_required
from ..models import Teacher, save, update, delete, role_required

namespace = Namespace("teachers", description="Operations on Teachers")

teacher_model = namespace.model(
    "TeacherX",
    {
        "name": fields.String(description="Teacher's name"),
        "email": fields.String(description="Teacher's email"),
        "role": fields.String(description="Teacher role")
    },
)
teacher_clone_model = namespace.clone(
    "Teacher", teacher_model, {"teacher_id": fields.Integer(description="Teacher ID"),
                               'courses': fields.List(fields.String())
                               }
)

course_model = namespace.model(
    "Courses",
    {
        "course_id": fields.Integer(description="Course ID"),
        "course_title": fields.String(description="Course Title"),
        "course_code": fields.String(description="Course code"),
        "description": fields.String(description="Course Description"),
        "credit_unit": fields.String(description="Course credit unit"),
        "teacher_id": fields.String(descriptiom="Course Teacher ID"),
    },
)


@namespace.route("/teacher")
class GetTeachers(Resource):

    @namespace.marshal_with(teacher_clone_model)
    @namespace.doc(
        description="Get all teachers in the Teacher database"
    )
    @jwt_required()
    # @role_required('teacher')
    def get(self):
        """Get all Teachers"""

        teachers = Teacher.query.filter_by(role='teacher').all()

        return teachers, 200


@namespace.route("/<int:teacher_id>/")
class GetUpdateDeleteTeacherandTeacherCourses(Resource):
    @namespace.marshal_with(course_model)
    @namespace.doc(
        description="Get all Courses taught by the specific Teacher",
        params = {
            'teacher_id': "ID of the specific teacher"
        }
    )
    @jwt_required()
    def get(self, teacher_id):
        """Get all Courses by Teacher ID

        Args:
            teacher_id (_int_): _ID of the Teacher_
        """
        teacher = Teacher.query.filter_by(teacher_id=teacher_id).first()
        if not teacher:
            abort(404, message="Teacher record not found")
        
        courses = teacher.courses

        return courses, 200
    @namespace.expect(teacher_model)
    @namespace.marshal_with(teacher_clone_model)
    @namespace.doc(
        description="Update Records of a Teacher using the Teacher ID",
        params = {
            'teacher_id': "ID of the specific teacher"
        }
    )
    @jwt_required()
    def put(self, teacher_id):
        """Update a Teacher Record from the Teacher database

        Args:
            teacher_id (_int_): Teacher ID
        """
        data = namespace.payload
        teacher = Teacher.query.filter_by(teacher_id=teacher_id).first()
        if not teacher:
            abort(404, message="Teacher Record not found")
        teacher.name = data['name']
        teacher.email = data['email']
        update(teacher)
        return teacher, 200
    
    @namespace.doc(
        description="Delete Records of a Teacher using the Teacher ID",
        params = {
            'teacher_id': "ID of the specific teacher"
        }
    )
    @jwt_required()
    def delete(self, teacher_id):
        """Delete a Teacher from the Teacher database

        Args:
            teacher_id (_int_): Teacher ID
        """
        teacher = Teacher.query.filter_by(teacher_id=teacher_id).first()
        if not teacher:
            abort(404, message="Teacher not found in database.")
        
        delete(teacher)
        return {"message": "Teacher Successfully deleted from teacher database."}
        
@namespace.route('/<int:teacher_id>/details')
class GetSpecificTeacher(Resource):
    
    @namespace.marshal_with(teacher_clone_model)
    @namespace.doc(description='Get a specific teacher by ID',
                   params={
                       "teacher_id":"ID of the teacher to get"
                   })
    @jwt_required()
    def get(self, teacher_id):
        """Get a specific Teacher by ID

        Args:
            teacher_id (_int_): ID of the Teacher
        """
        teacher = Teacher.query.filter_by(teacher_id=teacher_id).first()
        if not teacher:
            abort(404, message="Teacher record not found")
        
        return teacher, 200
    