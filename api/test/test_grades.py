import unittest
import json
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from .. import create_app
from ..config.config import config_dict
from ..db import db
from ..models import Student, Course, StudentCourse, save, update, delete


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
        token = create_access_token(identity='teststudent@test.io')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        student1 = Student(name='Test Student',
                           email='teststudent@test.com',
                           password_hash='password',
                           role="student"
                           )
        save(student1)
        
        course = Course(
            course_title="Test Course",
            course_code="TST101",
            description="This is a test course",
            credit_unit=3,
            teacher_id=1,
        )
        save(course)

        student_course = StudentCourse(
            student_id=student1.student_id,
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
        token = create_access_token(identity='teststudent@test.io')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        student1 = Student(name='Test Student',
                           email='teststudent@test.com',
                           password_hash='password',
                           role="student"
                           )
        save(student1)
        
        course = Course(
            course_title="Test Course",
            course_code="TST101",
            description="This is a test course",
            credit_unit=3,
            teacher_id=1,
        )
        save(course)

        student_course = StudentCourse(
            student_id=student1.student_id,
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