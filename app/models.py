from flask_sqlalchemy import SQLAlchemy
from . import db
from . import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, current_user
from datetime import datetime

import app

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")
    
    def __repr__(self):
        return f'User {self.name}'        



class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    pitches = db.relationship('Pitch',backref = 'user',lazy="dynamic")
    comments = db.relationship('Comment',backref = 'user',lazy="dynamic")
    upvote = db.relationship('Upvote',backref='user',lazy='dynamic')
    downvote = db.relationship('Downvote',backref='user',lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)
        
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def save_u(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()    

    def __repr__(self):
        return f'User {self.username}'

class Pitch(db.Model):
    __tablename__ = 'pitch'

    id = db.Column(db.Integer,primary_key = True)
    title =  db.Column(db.String(255)) 
    pitch_content = db.Column(db.String(255))
    author = db.Column(db.String(255))
    category = db.Column(db.String(255))
    upvote = db.Column(db.Integer)
    downvote = db.Column(db.Integer)
    published_at = db.Column(db.DateTime, default = datetime.utcnow)    
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    time = db.Column(db.DateTime, default = datetime.utcnow)
    comments = db.relationship('Comment',backref = 'pitch',lazy="dynamic")
    

    def __repr__(self):
        return f'User {self.description}'

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    body = db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id'))
            
    published_at = db.Column(db.DateTime, default = datetime.utcnow)  

    def __repr__(self):
        return f'User {self.description}'

class Upvote(db.Model):
    __tablename__ = 'upvotes'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_upvotes(cls,id):
        upvote = Upvote.query.filter_by(pitch_id=id).all()
        return upvote


    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'
class Downvote(db.Model):
    __tablename__ = 'downvotes'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    

    def save(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_downvotes(cls,id):
        downvote = Downvote.query.filter_by(pitch_id=id).all()
        return downvote

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'    

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)    


db.create_all()            