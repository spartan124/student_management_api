from flask_restx import Namespace, Resource, fields, abort

from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.student_course import StudentCourse
from ..models.courses import Course
from ..models.results import StudentResult


namespace = Namespace("grades", description='Operation on grades')

grades_model = namespace.model(
    "StudentCourse",  {
        "grade": fields.String(description='Student grade in course')
    }
)


@namespace.route('/student/<int:student_id>/course/<int:course_id>/add')
class Grade(Resource):
    @namespace.expect(grades_model)
    @namespace.marshal_with(grades_model)
    @namespace.doc(
        description="Add grade for a student enrolled course",
        params={
            "student_id":"ID of the Student",
            "course_id": "ID of the Course"
        }
    )
    @jwt_required()
    def post(self, student_id, course_id):
        """Add course grade for student

        Returns:
            _type_: _description_
        """
        data = namespace.payload
        
        grade = data['grade']
    
        student_course = StudentCourse.query.filter_by(
            student_id=student_id, course_id=course_id
        ).first()
        
        if not student_course:
            abort(404, message="Student Record not found ")
            
        course_grade = student_course.grade
        if course_grade:
            abort(403, message="Grade already exist for this student course")
            
        student_course.grade = grade
        
        student_course.save()
        return student_course, 201

@namespace.route('/student/<int:student_id>/course/<int:course_id>')
class StudentCourseGrade(Resource):
    @namespace.marshal_with(grades_model)
    @namespace.doc(
        description="Get grade for a student enrolled course",
        params={
            "student_id":"ID of the Student",
            "course_id": "ID of the Course"
        }
    )
    @jwt_required()
    def get(self, student_id, course_id):
        """Retrieve a specific student grade for a specific course

        Args:
            student_id (_int_): Student ID
            course_id (_int_): Course ID
        """
        
        student_course = StudentCourse.query.filter_by(
            student_id=student_id, course_id=course_id
        ).first()
        
        if not student_course:
            abort(404, message="Record not found for this course")
        
            
        student_course.grade

        return student_course, 200

    @namespace.expect(grades_model)
    @namespace.marshal_with(grades_model)
    @namespace.doc(
        description="Update a course grade for a student",
        params={
            "student_id":"ID of the student",
            "course_id":"ID of the course to update grade"
        }
    )
    @jwt_required()
    def put(self, student_id, course_id):
        """Update a student's course grade

        Args:
            student_id (_int_): ID of the student
            course_id (_int_): ID of the course
        """
        current_user = {"student_id": get_jwt_identity()}
        data = namespace.payload
        grade_to_update = StudentCourse.query.filter_by(student_id=student_id, course_id=course_id).first()
        if current_user['student_id'] == student_id:
            
            if not grade_to_update:
                abort(404, message="Course record not Found for this student")
            grade_to_update.grade = data['grade']
            grade_to_update.update()
            
            return 201, grade_to_update
        return {"message":"User not authorized to update grade record"}, 401