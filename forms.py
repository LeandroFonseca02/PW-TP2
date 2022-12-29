from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, ValidationError
from wtforms.validators import DataRequired, InputRequired, Length
from models import *

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Length(min=7, max=255)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=255)])

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Length(min=7, max=255)])
    phone = StringField('Telemóvel', validators=[InputRequired(), Length(min=7, max=30)])
    first_name = StringField('Nome Próprio', validators=[InputRequired(), Length(min=1, max=50)])
    last_name = StringField('Apelido', validators=[InputRequired(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=255)])
    confirm_password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=255)])

class RequestResetForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Length(min=7, max=255)])

    def validate_email(self, email):
        user = db.session.query(User).filter(User.email == email.data).first()
        if user is None:
            raise ValidationError('Não existe nenhuma conta com este email.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=255)])
    confirm_password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=255)])