from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, abort, fields
from flask import jsonify
from ..models import StudentCourse, StudentResult, Student

namespace = Namespace("result", description="Operation on Results")

results_model = namespace.model(
    "Result",
    {
        "course_id": fields.Integer(description="Course ID"),
        "course_code": fields.String(description="Course title", required=True),
        "course_title": fields.String(description="Course title", required=True),
        "credit_unit": fields.Integer(description="course credit unit", required=True),
        "grade": fields.String(description='Grade in Course'),
        "earned_credit": fields.String(description='Credit unit earned'),
        "gpa": fields.Float(description="Grade Point Average")
        
    }
)
gpa_model = namespace.model(
    'Result',
    {
        "gpa": fields.Float(description="Grade Point Average")
    }
)
@namespace.route('/student/<int:student_id>/gpa')
class AddStudeentGPA(Resource):
    @namespace.marshal_with(gpa_model)
    def post(self, student_id):
        """Add Student GPA

        Args:
            student_id (_int_): Student ID
        """
        student = Student.query.filter_by(student_id=student_id).first()
        
        if not student:
            abort(404, message="Student Record not found")
        student.gpa
        student.save()
        return {student}, 201
    
    def get(self, student_id):
        """Get result data via a result sheet

        Returns:
            _list_: Return student results record
        """
        student = Student.get_by_id(student_id)
        result_sheet = student.result_sheet()
        return jsonify({'result_sheet': result_sheet})
    
@namespace.route('/student/<int:student_id>/course/<int:course_id>')    
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
        
        if not sc:
            abort(404, message="Record not found")
            
        student_id = sc.student_id
        course_id = sc.course_id
        course_code = sc.course.course_code
        course_title = sc.course.course_title
        credit_unit = sc.course.credit_unit
        grade = sc.grade
        earned_credit = sc.earned_credit
        
        results = StudentResult.query.filter_by(student_id=student_id, course_id=course_id).first()   
        if results:
            abort(403, message="Record already exists for this student")
            
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
        if course is None:
            abort(404, message="Course record not found for this student")
        
        course.delete()
        return  {"message":"Result record successfully deleted"}, 204