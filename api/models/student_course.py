from ..db import db

class StudentCourse(db.Model):
    __tablename__= 'student_course'
    student_id = db.Column(db.Integer(), db.ForeignKey('students.student_id'), primary_key=True)
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.course_id'))
    grade = db.Column(db.String())
    earned_credit = db.Column(db.Float())
    gpa = db.Column(db.Float())
    
    #students = db.relationship('Student', back_populates='courses')
    course = db.relationship('Course', backref='student_course')
   
    
    def __repr__(self):
        return f"<Student Course ID {self.student_id}>"
    
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