import unittest

from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from .. import create_app
from ..config.config import config_dict
from ..db import db
from ..models import Student, Course, StudentCourse


class StudentTestCase(unittest.TestCase):
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

    def test_student_registration(self):
        data = {
            "email": "testuser@test.com",
            "password": "password",
            "name": "Student",
        }
        response = self.client.post("/auth/signup", json=data)
        user = Student.query.filter_by(email="testuser@test.com").first()
        assert user.email == "testuser@test.com"
        assert user.name == "Student"
        assert response.status_code == 201
        
        # test a failed signup request (duplicate email)
        data = {'name': 'Duplicate Student', 'email': 'testuser@test.com', 'password': 'duplicatepassword'}
        response = self.client.post('/auth/signup', json=data)
        self.assertEqual(response.status_code, 403)

    def test_student_login(self):
        email = 'testuser@test.com'
        password = 'password'
        password_hash = generate_password_hash(password)
        check_password = check_password_hash(password_hash, password)

        data = {
            'email': email,
            'password': check_password
        }


         # test a successful login request
        response = self.client.post('auth/login', json=data)

        assert response.status_code == 200
    
    def test_get_all_students(self):
        token = create_access_token(identity='teststudent@test.io')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        student1 = Student(name='Test Student',
                           email='teststudent@test.com',
                           password_hash='password'
                           )
        student1.save()
        student2 = Student(name='Fun Student',
                           email='funstudent@test.com',
                           password_hash='password'
                           )
        student2.save()
        
        #Test get all students
        response = self.client.get('/', headers=headers)
        student = Student.query.all()
        assert response.status_code == 200
        assert len(student) == 2
        assert student != []
        
    #Test enroll student to a course
    def test_enroll_student_to_course(self):
        token = create_access_token(identity='teststudent@test.io')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        student = Student(name='Test Student',
                           email='teststudent@test.com',
                           password_hash='password'
                           )
        student.save()  
        course = Course(
            course_id=1,
            course_title="Intro to Python",
            course_code="PY101",
            credit_unit=3,
            description="Beginners guide to python",
            teacher_id=1,
        )
        course.save()
        
        payload = {
            'student_id': student.student_id,
            'course_id': course.course_id
        }
        response = self.client.post("/students/{}/course/{}/enroll".format(student.student_id, course.course_id), 
                                    json=payload, headers=headers)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['student_id'], student.student_id)
        self.assertEqual(response.json['course_id'], course.course_id)
        
        enrolled = StudentCourse.query.filter_by(student_id=student.student_id, course_id=course.course_id).first()
        self.assertIsNotNone(enrolled)
        
        #Test duplicate enrollment
        response = self.client.post("/students/{}/course/{}/enroll".format(student.student_id, course.course_id), 
                                    json=payload, headers=headers)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json['message'], 'Student already enrolled in course')