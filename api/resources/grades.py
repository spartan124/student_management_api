from flask_restx import Namespace, Resource, fields, abort

from flask_jwt_extended import jwt_required
from ..models.student_course import StudentCourse
from ..models.courses import Course
from ..models.results import StudentResult


namespace = Namespace("grades", description='Operation on grades')

grades_model = namespace.model(
    "StudentCourse",  {
        "grade": fields.String(description='Student grade in course')
    }
)
results_model = namespace.model(
    "Result",
    {
        "course_id": fields.Integer(description="Course ID"),
        "course_code": fields.String(description="Course title", required=True),
        "course_title": fields.String(description="Course title", required=True),
        "credit_unit": fields.Integer(description="course credit unit", required=True),
        "grade": fields.String(description='Grade in Course'),
        "earned_credit": fields.String(description='Credit unit earned'),
        
    }
)

@namespace.route('/<int:student_id>/<int:course_id>/add')
class Grade(Resource):
    @namespace.expect(grades_model)
    @namespace.marshal_with(grades_model)
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
        # return {'message': f"Grade added for student {student_id} in  {course.course_code}"}, 201
        return student_course, 201

@namespace.route('/<int:student_id>/<int:course_id>')
class StudentCourseGrade(Resource):
    @namespace.marshal_with(grades_model)
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

    
@namespace.route('/results/<int:student_id>/<int:course_id>')    
class AddResults(Resource):
    @namespace.marshal_with(results_model)
    def post(self, student_id, course_id):
        """Collate Student Results

        Args:
            student_id (_int_): Student ID
            course_id (_int_): Course ID

        Returns:
            _dict_: returns a dict list of student results
        """
        sc = StudentCourse.query.filter_by(student_id=student_id, course_id=course_id).first()
        
        student_id = sc.student_id
        course_id = sc.course_id
        course_code = sc.course.course_code
        course_title = sc.course.course_title
        credit_unit = sc.course.credit_unit
        grade = sc.grade
        earned_credit = sc.earned_credit
        
        if not sc:
            return f"Student Record not found, Please confirm that student is enrolled for this course"
        results = StudentResult.query.filter_by(student_id=student_id, course_id=course_id).first()   
        if not results:
            results = StudentResult(
                    student_id=student_id, course_id=course_id, course_code=course_code, course_title=course_title,
                    credit_unit = credit_unit, grade=grade, earned_credit=earned_credit
            )
        
            results.save()
            return results, 201
        
    @jwt_required()   
    def delete(self, student_id, course_id):
        """Delete a specific student_course record

        Args:
            student_id (_int_): Student ID
            course_id (_type_): Course ID
        """
        course = StudentResult.query.filter_by(student_id=student_id, course_id=course_id).first()
        course.delete()
        return {'message': "Result record for student course with course id {course.course_id} deleted successfully"}
            
        
            