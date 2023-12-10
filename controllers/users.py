from flask import Blueprint, request, redirect
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import User

users = Blueprint('users', __name__, template_folder='templates')


@users.route('/updatePassword', methods=['POST'])
@login_required
def updatePassword():
    if request.method == 'POST':
        password = request.form.get('password')
        newPassword = request.form.get('newPassword')
        passwordConfirmation = request.form.get('passwordConfirmation')
        user = User.get_user_by_id(current_user.id)

        if check_password_hash(user.password, password):
            if newPassword == passwordConfirmation:
                User.update_password(current_user.id, generate_password_hash(newPassword, method='sha256'))
                return redirect("/profile")
            else:
                return "password desigual"
        else:
            return "password incorreta"
