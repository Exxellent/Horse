
from sqlalchemy import Column, String, Integer
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

from app import db

class User(db.Model, UserMixin):  
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    
    def set_password(self, password: str):
        self.password = generate_password_hash(password)


    def check_password(self, password: str):
        return check_password_hash(self.password, password)
    

