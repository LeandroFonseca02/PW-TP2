import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, jsonify
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from models import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/rides'
UPLOAD_FOLDER = './static/images/profilePictures/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'cena secreta'

login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return db.session.query(User).filter(User.id == id).first()



with app.app_context():
    db = SQLAlchemy(app)


@app.route('/', methods=['POST', 'GET'])
@login_required
def index():  # put application's code here
    return jsonify(id=current_user.id, email=current_user.email, password=current_user.password)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = db.session.query(User).filter(User.email == email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return "Login com sucesso"
            else:
                return "Password Invalida"
        else:
            return "Este email nao pertence a nenhuma conta"
    else:
        return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():  # put application's code here
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user = db.session.query(User).filter(User.email == email).first()
        if user:
            return "Email ja esta a ser utilizado"
        else:
            if password != confirm_password:
                return "Passwords diferentes"
            else:
                new_user = User(email=email, password=generate_password_hash(password, method='sha256'), active=True)
                db.session.add(new_user)
                db.session.commit()
                new_profile = Profile(user_id=new_user.id, first_name=firstname, last_name=lastname,
                                      registration_date=datetime.now(), photo='none', phone_number=phone,
                                      classification=5.0)
                db.session.add(new_profile)
                db.session.commit()
                login_user(new_user)
                return redirect('/')
    else:
        return render_template('criar-utilizador.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "User Logout"


@app.route('/profile', methods=['GET'])
@login_required
def profile():  # put application's code here
    print(current_user)
    return render_template('perfil.html')


@app.route('/uploadImage', methods=['POST'])
def uploadImage():  # put application's code here
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, filename))
        return "Foto uploaded"


if __name__ == '__main__':
    app.run(debug=True)
