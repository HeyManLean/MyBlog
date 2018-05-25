from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, BooleanField, PasswordField
from wtforms.validators import Required, Email


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')