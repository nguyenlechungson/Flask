import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()

# Tạo trang login
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Vui lòng nhập thông tin vào form này.'

# Tạo file log ghi nhận sự kiện trong webapp
from logging.handlers import RotatingFileHandler
import os



# Tạo hàm tạo ứng dụng, chúng ta có thể kiểm tra biến này để thiết lập cấu hình phù hợp cho nhật ký ứng dụng, Ghi nhật ký vào stdout hoặc file.

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app,db)
    login.init_app(app)

    #Đăng ký blueprint xử lý lỗi với ứng dụng.
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp,url_prefix='/errors')

    #Đăng ký blueprint trang chính, xác thực người dùng với ứng dụng.
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)


    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler('logs/myweb.log',maxBytes=10240,backupCount=10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s: %(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('MyWeb startup')

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler= RotatingFileHandler('logs/myweb.log',maxBytes=10240,backupCount=10)
            file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s: %(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('MyWeb startup')
    
    return app

from app import models