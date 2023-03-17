from ..db import db


class Student(db.Model):
    __tablename__ = "students"
    student_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.Text(), nullable=False)
    gpa = db.Column(db.Float())
    courses = db.relationship("Course", secondary="student_course")
    student_courses = db.relationship("StudentCourse", backref="students")

    # student_results = db.relationship('Course', secondary='student_results')
    def __repr__(self):
        return f"<Student {self.name}>"

    @property
    def gpa(self):
        total_credits = 0
        total_earned_credits = 0

        for course in self.courses:
            total_credits += course.credit_unit

        for student_course in self.student_courses:
            total_earned_credits += student_course.earned_credit

        if total_credits == 0:
            return 0
        else:
            gpa = total_earned_credits / total_credits

            return round(gpa * 4.0 / 5.0, 2)

    def result_sheet(self):
        result = []
        course_data = {}
        for course in self.courses:
            course_data = {
                "course_id": course.course_id,
                "course_code": course.course_code,
                "course_title": course.course_title,
                "credit_unit": course.credit_unit,
            }
            result.append(course_data)
        
        for st_course in self.student_courses:
            course_data2 = {
                'grade': st_course.grade,
                'earned_credit': st_course.earned_credit
            }
        
            result.append(course_data2)
        
        gpa_data = {"gpa": self.gpa}
        result.append(gpa_data)
        return result

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
