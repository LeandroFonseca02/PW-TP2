from flask import render_template, Blueprint, redirect
from flask_login import login_required, current_user, logout_user, login_user, LoginManager
from werkzeug.security import check_password_hash, generate_password_hash

from forms import RegisterForm, LoginForm, RequestResetForm, ResetPasswordForm
from models.profile import Profile
from models.user import User
from utils import sendRecoverPasswordEmail

auth = Blueprint('auth', __name__, template_folder='templates')

login_manager = LoginManager()
login_manager.login_view = '/login'

@login_manager.user_loader
def load_user(id):
    return User.get_user_by_id(id)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()

    if form.is_submitted():
        email = form.email.data
        password = form.password.data
        user = User.get_user_by_email(email)
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect('/')
            else:
                return "Password Invalida"
        else:
            return "Este email nao pertence a nenhuma conta"
    else:
        return render_template('login.html',form=form)


@auth.route('/register', methods=['POST', 'GET'])
def register():  # put application's code here
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if form.is_submitted():
        email = form.email.data
        firstname = form.first_name.data
        lastname = form.last_name.data
        phone = form.phone.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        user = User.get_user_by_email(email)
        if user:
            return "Email ja esta a ser utilizado"
        else:
            if password != confirm_password:
                return "Passwords diferentes"
            else:
                user = User.create_user(email,generate_password_hash(password, method='sha256'))
                Profile.create_profile(user.id,firstname,lastname,phone)
                login_user(user)
                return redirect('/')
    else:
        return render_template('criar-utilizador.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect('/')
    form = RequestResetForm()
    if form.is_submitted():
        user = User.get_user_by_email(form.email.data)
        sendRecoverPasswordEmail(user)
        return redirect('/login')
    return render_template('reset_request.html', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect('/')
    user_id = User.verify_reset_token(token)
    if user_id is None:
        print('Token inválido ou expirado')
        return redirect('/reset_password')
    form = ResetPasswordForm()

    if form.is_submitted():
        password = form.password.data
        confirm_password = form.confirm_password.data
        if password != confirm_password:
            return "Passwords diferentes"
        else:
            User.update_password(user_id, generate_password_hash(password, method='sha256'))
            return redirect('/login')

    return render_template('reset_token.html', form=form)



