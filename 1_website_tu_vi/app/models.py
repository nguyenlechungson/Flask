from datetime import datetime
from app import db,login
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import app



# Lớp thông tin gia chủ
class UserDb(UserMixin,db.Model):
    __tablename__='user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64))
    birthday = db.Column(db.String(64))
    password_hash = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    email = db.Column(db.String(64),index=True,unique=True)
    phone = db.Column(db.String(64))
    address = db.Column(db.String(64))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    destination =db.relationship('UserDestination',backref='author',lazy='dynamic')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self,birthday):
        self.password_hash = generate_password_hash(birthday)
    
    def check_password(self,birthday):
        return check_password_hash(self.password_hash,birthday)

@login.user_loader
def load_user(id):
    return UserDb.query.get(int(id))
   

#Lớp Thông tin tử vi
class UserDestination(db.Model):
    __tablename__='destination'
    id = db.Column(db.Integer, primary_key=True)
    menh = db.Column(db.String())
    tam_tai = db.Column(db.String())
    kim_lau = db.Column(db.String())
    hoang_oc = db.Column(db.String())
    nam_thuan_loi = db.Column(db.String())
    can_chi = db.Column(db.String())
    nam_sinh_am_lich = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return '<Mệnh {}>'.format(self.menh)


#Lớp thông tin ý kiến phản hồi
class Post(db.Model):
    __tablename__='post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime,nullable=False,default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    
    def __str__(self):
        return '<Post {}>'.format(self.title)
