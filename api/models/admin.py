from ..db import db

class Admin(db.Model):
    __tablename__ = 'admins'
    admin_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email= db.Column(db.String(), unique=True, nullable=False)
    role = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.Text(), nullable=False)
    
    def __repr__(self):
        return f"{self.name}"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    