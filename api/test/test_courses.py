import json
import unittest

from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash, generate_password_hash

from .. import create_app
from ..config.config import config_dict
from ..db import db
from ..models import Course, Student, StudentCourse, save
from ..resources.courses import clone_course_model


class CoursesTestCase(unittest.TestCase):
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
        
    def test_add_course(self):
        
        #Generate access_token
        token = create_access_token(identity='teststudent@test.io')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        #Test adding a course
        course_data = {
            "course_title": "Test Course",
            "course_code": "TEST101",
            "description": "This is a test course",
            "credit_unit": 3,
            "teacher_id": 1
        }
        response = self.client.post('/course/', json=course_data, headers=headers)
        self.assertEqual(response.status_code, 201)

        # Test adding a course with same course code again
        response = self.client.post('/course/', json=course_data, headers=headers)
        self.assertEqual(response.status_code, 403)
        
        #Test get all courses
        response = self.client.get('/course/', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        
    def test_get_courses(self):
        token = create_access_token(identity='teststudent@test.io')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        course = Course(
            course_title="Test Course",
            course_code="TC",
            description="A test course",
            credit_unit=3,
            teacher_id=1,
        )
        course.save()
        response = self.client.get("/course/{}".format(course.course_id), headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['course_id'], course.course_id)
        self.assertEqual(response.json['course_code'], course.course_code)
        
        
        #Test course not found
        response = self.client.get("/course/99", headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_update_course(self):
        token = create_access_token(identity='teststudent@test.io')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        course = Course(
            course_title="Test Course",
            course_code="TEST101",
            description="This is a test course",
            credit_unit=3,
            teacher_id=1,
        )
        course.save()

        data = {
            "course_title": "Updated Test Course",
            "course_code": "TEST102",
            "description": "This is an updated test course",
            "credit_unit": 4,
            "teacher_id": 2,
        }
        response = self.client.put("/course/{}".format(course.course_id), headers=headers, json=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, "application/json")
        
        updated_course = Course.query.filter_by(course_id=course.course_id).first()
        
        self.assertEqual(updated_course.course_title, data["course_title"])
        self.assertEqual(updated_course.course_code, data["course_code"])
        self.assertEqual(updated_course.description, data["description"])
        self.assertEqual(updated_course.credit_unit, data["credit_unit"])
        self.assertEqual(updated_course.teacher_id, data["teacher_id"])
    
    def test_delete_a_course(self):
        token = create_access_token(identity='teststudent@test.io')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        course = Course(
            course_title="Mathematics",
            course_code="MAT101",
            description="An introductory math course",
            credit_unit=3,
            teacher_id=1,
        )
        course.save()
            
        response = self.client.delete("/course/{}".format(course.course_id), headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["message"], "Course successfully deleted")

    def test_enrolled_students(self):
        token = create_access_token(identity='teststudent@test.io')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        
        
        student1 = Student(name='Test Student',
                           email='teststudent@test.com',
                           password_hash='password',
                           role='student'
                           )
        save(student1)
        student2 = Student(name='Fun Student',
                           email='funstudent@test.com',
                           password_hash='password',
                           role='student'
                           )
        save(student2)
        
        course = Course(
            course_title="Test Course",
            course_code="TST101",
            description="This is a test course",
            credit_unit=3,
            teacher_id=1,
        )
        save(course)

        student_course1 = StudentCourse(
            course_id=course.course_id,
            student_id=student1.student_id
        )
        save(student_course1)
        
        student_course2 = StudentCourse(
            course_id=course.course_id,
            student_id=student2.student_id
        )
        save(student_course2)
        
        response = self.client.get("/course/{}/students".format(course.course_id), headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        
        print(response.json)