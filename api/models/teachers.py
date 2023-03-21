from ..db import db


class Teacher(db.Model):
    __tablename__ = "teachers"
    teacher_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    role = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.Text(), nullable=False)
    courses = db.relationship('Course', backref='student_courses')
    def __repr__(self):
        return f"<Teacher {self.name}>"
    
    # def save(self):
    #     db.session.add(self)
    #     db.session.commit()
        
    # def update(self):
    #     db.session.commit()
        
    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()
        
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)