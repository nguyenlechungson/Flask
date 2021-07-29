from wtforms import validators
from app.models import UserDb
from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,SelectField,TextAreaField,IntegerField
from wtforms.validators import DataRequired, Email,Length, NumberRange, ValidationError
from flask import flash


class FormThongTinGiaChu(FlaskForm):
    username = StringField('Họ tên',validators=[DataRequired()])
    birthday = StringField('Ngày sinh', validators=[DataRequired()])
    gender = SelectField('Giới tính',choices=['Nam','Nữ'])
    email = StringField('Email',validators=[DataRequired(),Email()])
    #phone = IntegerField('Điện thoại',validators=[NumberRange(message='[Lỗi nhập liệu. điện thoại chỉ con số 0->9]')])
    address = StringField('Địa chỉ')
    submit = SubmitField("Xem kết quả")

    def validate_email(self,email):
        user = UserDb.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email đã được đăng ký. Vui lòng chọn email khác.')
    
    def validate_username(self,username):
        user = UserDb.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Họ tên đã được đăng ký. Vui lòng chọn tên khác.')

    def validate_birthday(self,birthday):
        year,month,day = birthday.data.split('-')
        year = int(year)
        if year < 1900:
            raise ValidationError('Vui lòng nhập lại [ từ năm 1900 trở đi ].')


# Tạo Form lấy ý kiến
class PostForm(FlaskForm):
    username = StringField('Họ và tên',[validators.Required("Nhập họ tên.")])
    email = StringField('Email',validators=[DataRequired(),Email()]) 
    post = TextAreaField('Nội dung ..',validators=[DataRequired(),Length(min=1,max=4000)])
    submit = SubmitField('Gửi nội dung')

    def validate_email(self,email):
        user = UserDb.query.filter_by(email = email.data).first()

        if user is None:
            raise ValidationError('Email này chưa được đăng ký ! Vui lòng nhập Form thông tin gia chủ và nhấn Xem kết quả để cập nhật thông tin')
        
        
#Form đăng nhập
class LoginForm(FlaskForm):
    username = StringField('Họ và tên',[validators.Required("Nhập họ tên.")])
    birthday = StringField('Ngày/tháng/năm sinh', validators=[DataRequired()])
    submit = SubmitField('Đăng nhập')

    