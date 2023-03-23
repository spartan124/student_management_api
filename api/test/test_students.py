import unittest

from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from .. import create_app
from ..config.config import config_dict
from ..db import db
from ..models import Student, Course, StudentCourse, save, update, delete
from . import create_student, create_course, create_teacher


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
            "role":"student"
        }
        response = self.client.post("/auth/student/signup", json=data)
        user = Student.query.filter_by(email="testuser@test.com").first()
        assert user.email == "testuser@test.com"
        assert user.name == "Student"
        assert response.status_code == 201
        
        # test a failed signup request (duplicate email)
    def test_duplicate_student_registration(self):
        student = create_student()
        save(student)
        data = {'name': 'Duplicate Student', 'email': 'teststudent@test.com', 'password': 'duplicatepassword', 'role':'student'}
        response = self.client.post('/auth/student/signup', json=data)
        self.assertEqual(response.status_code, 403)

    def test_user_login(self):
        email = 'testuser@test.com'
        password = 'password'
        password_hash = generate_password_hash(password)
        check_password = check_password_hash(password_hash, password)

        data = {
            'email': email,
            'password': check_password
        }


        #Test a successful login request
        response = self.client.post('auth/login', json=data)

        assert response.status_code == 200
    
    def test_get_all_students(self):
        student = create_student()
        token = create_access_token(identity=student.email, additional_claims={'role': 'admin'})
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        save(student)
        student2 = create_student(name="fun student", email="funstud@test.com", password_hash='password', role='student')
        save(student2)
        
        #Test get all students
        response = self.client.get('/students/', headers=headers)
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
        student = create_student()
        save(student)  
        
        course = create_course()
        save(course)
        
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
        
        #Test get enrolled courses
        response = self.client.get('/students/{}/courses'.format(student.student_id), headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['course_code'], 'TST101')
        
        
        #Test get student detail
        student = Student.query.filter_by(student_id=1).first()
        response = self.client.get('/students/1/details')
        data = response.json
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['student_id'], 1)
        self.assertEqual(data['name'], 'Test Student')
        self.assertEqual(data['email'], 'teststudent@test.com')
        self.assertEqual(data['gpa'], student.gpa)
        
        
        
        
        
        