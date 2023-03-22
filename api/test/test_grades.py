import unittest
import json
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from .. import create_app
from ..config.config import config_dict
from ..db import db
from ..models import Student, Course, StudentCourse, save, update, delete
from . import create_course, create_student, create_teacher


class GradeTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict["test"])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.client = None

    def test_add_student_grade(self):
        
        teacher = create_teacher()
        save(teacher)
        
        token = create_access_token(identity=teacher.email, additional_claims={'role': 'teacher'})
        headers = {
            'Authorization': f'Bearer {token}'
        }
        student = create_student() #student data in __init__.py
        save(student)
        
        course = create_course()
        save(course)

        student_course = StudentCourse(
            student_id=student.student_id,
            course_id=course.course_id
        )
        save(student_course)
        
        payload = {
            "grade": "A"
        }
        response = self.client.post('/grades/student/{}/course/{}/add'.format(student_course.student_id, student_course.course_id),
                                    headers=headers, json=payload
                                    )
        assert response.status_code == 201
        returned_student_course = json.loads(response.data)
        assert returned_student_course['grade'] == "A"
        
    def test_get_student_grade_in_course(self):
        student = create_student()
        save(student)
        
        token = create_access_token(identity=student.email)
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        
        course = create_course()
        save(course)

        student_course = StudentCourse(
            student_id=student.student_id,
            course_id=course.course_id, grade="A"
        )
        save(student_course)
        response = self.client.get('/grades/student/{}/course/{}'.format(
            student_course.student_id, student_course.course_id), headers=headers,
        )
        self.assertEqual(response.status_code, 200)
        
        data = response.json
        self.assertEqual(data['grade'], "A")
        
    def test_get_student_course_grade_not_found(self):
        response = self.client.get('/student/999/course/999')
        
        self.assertEqual(response.status_code, 404)