import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, url_for, request, redirect, jsonify
from models import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/rides'
UPLOAD_FOLDER = './static/images/profilePictures/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
with app.app_context():
    db = SQLAlchemy(app)


@app.route('/', methods=['POST', 'GET'])
def index():  # put application's code here
    if request.method == 'POST':
        email = request.form.get('email'),
        firstname = request.form.get('firstname'),
        lastname = request.form.get('lastname'),
        phone = request.form.get('phone'),
        password = request.form.get('password'),
        confirm_password = request.form.get('confirm_password')

        # registration = request.get_json()
        # print(registration)
        registration_data = request.get_data()
        print(registration_data)

        return email
        # user = db.session.query(Role).all()
        # db.session.commit()
    else:
        user = db.session.query(User).all()
        return user


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        return jsonify(email=email,password=password)

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
        # registration = request.get_json()
        # print(registration)
        registration_data = request.get_data()
        print(registration_data)

        return jsonify(email = request.form.get('email'),
        firstname = request.form.get('firstname'),
        lastname = request.form.get('lastname'),
        phone = request.form.get('phone'),
        password = request.form.get('password'),
        confirm_password = request.form.get('confirm_password'))
        # user = db.session.query(Role).all()
        # db.session.commit()
    else:
        return render_template('criar-utilizador.html')


@app.route('/profile', methods=['GET'])
def profile():  # put application's code here
    return render_template('perfil.html')


@app.route('/profileData<int:id>', methods=['GET'])
def get_profile_data(id):  # put application's code here
    user = db.session.query(User).filter(User.id == id).all()
    return jsonify(user)



@app.route('/uploadImage', methods=['POST'])
def uploadImage():  # put application's code here
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER,filename))
        return "Foto uploaded"


if __name__ == '__main__':
    app.run(debug=True)
