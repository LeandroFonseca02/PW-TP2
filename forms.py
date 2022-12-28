from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, InputRequired, Length

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Length(min=7, max=30)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=50)])

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Length(min=7, max=30)])
    phone = StringField('Telemóvel', validators=[InputRequired(), Length(min=7, max=30)])
    first_name = StringField('Nome Próprio', validators=[InputRequired(), Length(min=1, max=50)])
    last_name = StringField('Apelido', validators=[InputRequired(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=50)])
    confirm_password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=50)])
