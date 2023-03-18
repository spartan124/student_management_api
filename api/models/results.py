from ..db import db


class StudentResult(db.Model):
    __tablename__ = "student_results"
    
    student_id = db.Column(db.Integer(), db.ForeignKey("student_course.student_id"), primary_key=True)
    course_id = db.Column(db.Integer(), db.ForeignKey("student_course.course_id"), primary_key=True)
    course_code = db.Column(db.String(), nullable=False)
    course_title = db.Column(db.String(), nullable=False)
    credit_unit = db.Column(db.Integer(), nullable=False)
    grade = db.Column(db.String(2), nullable=False)
    earned_credit = db.Column(db.Integer(), nullable=False)
    
    def __repr__(self):
        return f"{self.id}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()