from ..models import Admin, Teacher, Student, Course, StudentCourse, StudentResult


def create_course(course_title="Test Course", course_code="TST101", description="This is a test course", credit_unit=3, teacher_id=1):
    course = Course(
        course_title=course_title,
        course_code=course_code,
        description=description,
        credit_unit=credit_unit,
        teacher_id=teacher_id
    )
    return course

def create_student():
    student = Student(
        name='Test Student',
        email='teststudent@test.com',
        password_hash='password',
        role='student'
    )
    return student


def create_teacher():
    teacher = Teacher(
        name='Test Teacher',
        email='testteacher@test.com',
        password_hash='password',
        role='teacher'
    )
    return teacher

