
import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin



from app import db, app

class User(db.Model, UserMixin):  
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)    
    login = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    role_id = db.Column(db.Integer)    
    
    def set_password(self, password: str):
        self.password = generate_password_hash(password)


    def check_password(self, password: str):
        return check_password_hash(self.password, password)
    @property
    def is_admin(self):
        return app.config.get('ADMIN_ROLE_ID') == self.role_id
    
class Horse(db.Model):
    __tablename__ = 'horses'
    
    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(50), nullable=False)
    count_win = db.Column(db.Integer, nullable=False)

class Jockey(db.Model):
    __tablename__ = 'jockeys'
    
    id = db.Column(db.Integer, primary_key=True)    
    full_name = db.Column(db.String(50), nullable=False)
    number_of_races = db.Column(db.String(20), nullable=True)
    
class Stat_race(db.Model):
    __tablename__ = 'stat_race'
    
    id = db.Column(db.Integer, primary_key=True)    
    date = db.Column(db.DateTime, nullable=False, server_default=sa.sql.func.now())
    f_place = db.Column(db.String(20), nullable=True)
    s_place= db.Column(db.String(20), nullable=True)
    t_place = db.Column(db.String(20), nullable=True)
    

    


