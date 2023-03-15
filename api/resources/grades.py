from flask_restx import Namespace, Resource, fields
from flask import abort
from ..models.student_course import StudentCourse
from ..models.courses import Course
from ..models.results import StudentResult


namespace = Namespace("grades", description='Operation on grades')

grades_model = namespace.model(
    "Grades",
    {
        # "course_id": fields.Integer(description='Course ID'),
        # 'student_id': fields.Integer(description='Student ID', required=True),
        'grade': fields.String(description='Student grade in course'),
        'earned_credit': fields.Integer(description='student earned credits')
    }
)
results_model = namespace.model(
    "Results",
    {
        "course_id": fields.Integer(description="Course ID"),
        "course_code": fields.String(description="Course title", required=True),
        "course_title": fields.String(description="Course title", required=True),
        "credit_unit": fields.Integer(description="course credit unit", required=True),
        'grade': fields.String(description='Grade in Course'),
        'earned_credit': fields.String(description='Credit unit earned'),
        
    }
)

@namespace.route('/<int:student_id>/<int:course_id>/add')
class Grade(Resource):
    @namespace.expect(grades_model)
    def post(self, student_id, course_id):
        """Add course grade for student

        Returns:
            _type_: _description_
        """
        data = namespace.payload
        
        grade = data['grade']
        # earned_credit = student_course.earned_credit
        course = Course.get_by_id(course_id)
        
        student_course = StudentCourse.query.filter_by(
            student_id=student_id, course_id=course_id
        ).first()
        
        earned_credit = student_course.earned_credit
        if not student_course:
            abort(404, f"Student with Student ID {student_id} not enrolled in {course.course_code}")
            
        student_course.grade = grade
        
        
        student_course.save()
        print(earned_credit)
        return {'message': f"Grade added for student {student_id} in  {course.course_code}"}, 201

@namespace.route('/<int:student_id>/<int:course_id>')
class StudentCourseGrade(Resource):
    def get(self, student_id, course_id):
        """Retrieve a specific student grade for a specific course

        Args:
            student_id (_int_): Student ID
            course_id (_int_): Course ID
        """
        course = Course.get_by_id(course_id)
        
        student_course = StudentCourse.query.filter_by(
            student_id=student_id, course_id=course_id
        ).first()
        
        if not student_course:
            abort(404, f"Student {student_id} not enrolled in course {course.course_code}")
            
        grade = student_course.grade
        earned_credit = student_course.earned_credit
        gpa = student_course.gpa
        return f"Student with ID {student_id} got Grade {grade} and earned {earned_credit} credits in {course.course_code} with  {gpa} GPA" 
    
@namespace.route('/results/<int:student_id>/<int:course_id>')    
class AddResults(Resource):
    @namespace.marshal_with(results_model)
    def post(self, student_id, course_id):
        
        sc = StudentCourse.query.filter_by(student_id=student_id, course_id=course_id).first()
        course_id = sc.course_id
        if not sc:
            abort(f"Student Record not found, Please confirm that student is enrolled for this course")
            
        if course_id:
            abort(f"Result already added for this student course")
        else:
            student_id = sc.student_id
            course_id = sc.course_id
            course_code = sc.course.course_code
            course_title = sc.course.course_title
            credit_unit = sc.course.credit_unit
            grade = sc.grade
            earned_credit = sc.earned_credit
        
            results = StudentResult(
                    student_id=student_id, course_id=course_id, course_code=course_code, course_title=course_title,
                    credit_unit = credit_unit, grade=grade, earned_credit=earned_credit
            )
        
            results.save()
            return results
        
        
    def delete(self, student_id, course_id):
        course = StudentResult.query.filter_by(student_id=student_id, course_id=course_id).first()
        course.delete()
        return {'message': "Result record for student course with course id {course.course_id} deleted successfully"}
            
        
            