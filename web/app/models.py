
from sqlalchemy import Column, String, Integer
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


from app import db

class User(db.Model, UserMixin):  
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)    
    login = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    
    def set_password(self, password: str):
        self.password = generate_password_hash(password)


    def check_password(self, password: str):
        return check_password_hash(self.password, password)
    
class Horse(db.Model):
    __tablename__ = 'horses'
    
    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(50), nullable=False)
    


