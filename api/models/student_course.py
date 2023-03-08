from ..db import db

class StudentCourse(db.Model):
    __tablename__= 'student_course'
    student_id = db.Column(db.Integer(), db.ForeignKey('students.student_id'), primary_key=True)
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.course_id'), primary_key=True)
    #grade = db.Column(db.String(), nullable=False)
    #credit_unit = db.Column(db.Float(), nullable=False)
    #earned_credit = db.Column(db.Float(), nullable=True)
    #teacher = db.relationship('Teacher', secondary='courses', backref='student_courses')
    
    def __repr__(self):
        return f"<Student Course ID {self.id}>"
    
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