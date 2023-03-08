from ..db import db



class Course(db.Model):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer(), primary_key=True)
    course_title = db.Column(db.String(100), nullable=False)
    course_code = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=True)
    credit_unit = db.Column(db.Integer(), nullable=False)
    teacher_id = db.Column(db.Integer(), db.ForeignKey('teachers.teacher_id'))
    
    def __repr__(self):
        return f"<Course {self.id}>"
    
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
    