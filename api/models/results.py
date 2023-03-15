from ..db import db


class StudentResult(db.Model):
    __tablename__ = "student_results"
    # id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey("students.student_id"), primary_key=True)
    course_id = db.Column(db.Integer(), db.ForeignKey("courses.course_id"), primary_key=True)
    course_code = db.Column(db.String(), nullable=False)
    course_title = db.Column(db.String(), nullable=False)
    credit_unit = db.Column(db.Integer(), nullable=False)
    grade = db.Column(db.String(2), nullable=False)
    earned_credit = db.Column(db.Integer(), nullable=False)
    # student_gpa = db.Column(db.Float())

    def __repr__(self):
        return f"{self.id}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()