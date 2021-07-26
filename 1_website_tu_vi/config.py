import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('web_dich_vu') or 'rat_kho_doan_@'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')or 'sqlite:///'+os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False