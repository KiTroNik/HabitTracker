from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(min=4, max=40)])
    password = PasswordField('Password', [DataRequired()])
    remember_me = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(min=4, max=40)])
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired(), EqualTo('confirm', message='Passwords must mach')])
    confirm = PasswordField('Repeat Password', [DataRequired()])
