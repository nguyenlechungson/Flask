import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('web_dich_vu') or 'rat_kho_doan_@'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')or 'sqlite:///'+os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    #kết nối database postgres trên Heroku với SQLAlchemy 1.4.x
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://","postgresql://",1)