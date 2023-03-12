from flask_restx import Namespace, Resource, fields
from flask import abort
from ..models.student_course import StudentCourse

namespace = Namespace("grades", description='Operation on grades')

grades_model = namespace.model(
    "Grades",
    {
        "course_id": fields.Integer(description='Course ID'),
        'student_id': fields.Integer(description='Student ID', required=True),
        'grade': fields.String(description='Student grade in course')
    }
)

namespace.route('/grades')
class Grade(Resource):
    @namespace.expect(grades_model)
    def post(self):
        """Add course grade for student

        Returns:
            _type_: _description_
        """
        data = namespace.payload
        student_id = data['student_id']
        course_id = data['course_id']
        grade = data['grade']
        
        student_course = StudentCourse.query.filter_by(
            student_id=student_id, course_id=course_id
        ).first()
        
        if not student_course:
            abort(404, f"Student {student_id} not enrolled in course {course_id}")
            
        student_course.grade = grade
        
        student_course.update()
        
        return {'message': f"Grade added for student {student_id} in course {course_id}"}, 201