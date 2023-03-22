from ..models import Admin, Teacher, Student, Course, StudentCourse, StudentResult
from werkzeug.security import generate_password_hash

def create_course(course_title="Test Course", course_code="TST101", description="This is a test course", credit_unit=3, teacher_id=1):
    course = Course(
        course_title=course_title,
        course_code=course_code,
        description=description,
        credit_unit=credit_unit,
        teacher_id=teacher_id
    )
    return course

def create_student(name='Test Student', email='teststudent@test.com', password_hash=generate_password_hash('password'), role='student'):
    student = Student(
        name=name,
        email=email,
        password_hash=password_hash,
        role=role
    )
    return student


def create_teacher(name='Test Teacher', email='testteacher@test.com', password_hash=generate_password_hash('password'), role='teacher'):
    teacher = Teacher(
        name=name,
        email=email,
        password_hash=password_hash,
        role=role
    )
    return teacher

