import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)

from flask_login import LoginManager


# Tạo trang login
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'Vui lòng nhập thông tin vào form này.'

# Tạo file log ghi nhận sự kiện trong webapp
from logging.handlers import RotatingFileHandler
import os

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/myweb.log',maxBytes=10240,backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s: %(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('MyWeb startup')

from app import routes, models, errors