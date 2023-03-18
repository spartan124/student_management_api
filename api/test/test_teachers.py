import unittest

from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash, generate_password_hash

from .. import create_app
from ..config.config import config_dict
from ..db import db
from ..models.courses import Course
from ..models.teachers import Teacher


class TeacherTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict["test"])
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()
        self.client = self.app.test_client()
        

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.client = None

    def test_add_teacher(self):
        token = create_access_token(identity='jones@schoolteacher.io')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        data = {"name": "Mr Jones", "email": "jones@schoolteacher.io"}

        response = self.client.post("/teachers/teacher", json=data, headers=headers)
        teacher = Teacher.query.filter_by(email="jones@schoolteacher.io").first()
        assert response.status_code == 201
        assert teacher.email == "jones@schoolteacher.io"
        assert teacher.teacher_id == 1
        

    def test_get_courses_by_teacher_id(self):
        # Add Teacher to database
        token = create_access_token(identity='jones@schoolteacher.io')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        data = {
            'name': "Mr. Jones",
            'email': "mrjones@school.io"
        }
        response =self.client.post('/teachers/teacher', json=data, headers=headers)
        teacher = Teacher.query.filter_by(teacher_id=1).first()
        assert teacher.courses == []
        #Test get teacher courses
        
        course1 = Course(
            course_id=1,
            course_title="Intro to Python",
            course_code="PY101",
            credit_unit=3,
            description="Beginners guide to python",
            teacher_id=1,
        )

        course2 = Course(
            course_id=2,
            course_title="Intro to python datastructures",
            course_code="PY103",
            credit_unit=3,
            description="Introduction to DSA",
            teacher_id=1,
        )
        teacher.courses = [course1, course2]
        teacher.save()
        
        response = self.client.get("teachers/{}/".format(teacher.teacher_id), headers=headers)

        
        assert response.status_code == 200
        assert response.json[0]['course_id'] == 1
        assert response.json[0]['course_code'] == "PY101"
        assert response.json[1]['course_id'] == 2
        assert response.json[1]['course_code'] == "PY103"
        
        # Test get_teacher with wrong teacher_id
        response = self.client.get("teachers/88/details", headers=headers) 
        assert response.status_code == 404
        assert response.json['message'] == "Teacher record not found"
        # Test delete teacher
        response = self.client.delete('/teachers/{}/'.format(teacher.teacher_id), headers=headers)
        get_teacher = Teacher.query.filter_by(teacher_id=teacher.teacher_id).first()
        assert response.status_code == 200
        assert response.json['message'] == "Teacher Successfully deleted from teacher database."
        assert get_teacher is None