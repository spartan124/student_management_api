import unittest

from werkzeug.security import check_password_hash, generate_password_hash

from .. import create_app
from ..config.config import config_dict
from ..db import db
from ..models.teachers import Teacher
from ..models.courses import Course


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

    def test_add_teacher(self):
        data = {
            'name': "Mr Jones",
            'email': "jones@schoolteacher.io"
        }

        response = self.client.post('/teachers/teacher', json=data)
        teacher = Teacher.query.filter_by(name="Mr Jones").first()
        assert teacher.email == "jones@schoolteacher.io"
        assert response.status_code == 201

    def test_get_teacher_courses(self):
        teacher = Teacher(teacher_id=1, name="Mr Jones", email="mrjones@school.io")
        teacher.save()
        
        course1 = Course(course_id=1,course_title="Intro to Python", course_code="PY101", credit_unit=3, description="Beginners guide to python", teacher_id=1)
        course1.save()

        course2 = Course(course_id=2,course_title="Intro to python datastructures", course_code="PY103", credit_unit=3, description="Introduction to DSA", teacher_id=1)
        course2.save()

        all_teacher = Teacher.query.filter_by(teacher_id=1).first()
        response = self.client.get('teachers/<int:teacher_id>/courses', json=all_teacher)

        all_teacher = Teacher.query.filter_by(teacher_id=1).first()

        assert len(all_teacher.courses) == 2
        assert response.status_code == 200
