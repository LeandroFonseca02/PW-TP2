from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, DateField, TimeField, \
    IntegerField, TextAreaField
from wtforms.validators import InputRequired, Length, Optional

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Length(min=7, max=255)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=255)])

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Length(min=7, max=255)])
    phone = StringField('Telemóvel', validators=[InputRequired(), Length(min=9, max=30)])
    first_name = StringField('Nome Próprio', validators=[InputRequired(), Length(min=1, max=50)])
    last_name = StringField('Apelido', validators=[InputRequired(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=255)])
    confirm_password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=255)])

class RequestResetForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Length(min=7, max=255)])



class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=255)])
    confirm_password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=255)])


class SearchRideForm(FlaskForm):
    inputOrigem = StringField('Origem', validators=[InputRequired(), Length(min=1, max=50)])
    inputDestino = StringField('Destino', validators=[InputRequired(), Length(min=1, max=50)])
    inputData = DateField('Data', validators=[InputRequired()])
    inputHora = TimeField('Hora', validators=[InputRequired()])


class CreateRideForm(FlaskForm):
    availableSeats = IntegerField('Lugares Disponíveis', validators=[InputRequired()])
    origin = StringField('Origem', validators=[InputRequired(), Length(min=1, max=50)])
    destination = StringField('Destino', validators=[InputRequired(), Length(min=1, max=50)])
    date = DateField('Data', validators=[InputRequired()])
    hour = TimeField('Hora', validators=[InputRequired()])
    description = TextAreaField('Descrição', validators=[Optional()])


class UpdateProfileDataForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Length(min=7, max=255)])
    phone = StringField('Telemóvel', validators=[InputRequired(), Length(min=9, max=30)])
    firstname = StringField('Nome Próprio', validators=[InputRequired(), Length(min=1, max=50)])
    lastname = StringField('Apelido', validators=[InputRequired(), Length(min=1, max=50)])


class CreateVehicleForm(FlaskForm):
    brand = StringField('Marca', validators=[InputRequired(), Length(min=1, max=50)])
    model = StringField('Modelo', validators=[InputRequired(), Length(min=1, max=50)])
    color = StringField('Cor', validators=[InputRequired(), Length(min=1, max=20)])
    licensePlate = StringField('Matrícula', validators=[InputRequired(), Length(min=8, max=20)])


class UpdatePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=255)])
    newPassword = PasswordField('Nova Password', validators=[InputRequired(), Length(min=8, max=255)])
    passwordConfirmation = PasswordField('Confirmar Password', validators=[InputRequired(), Length(min=8, max=255)])
