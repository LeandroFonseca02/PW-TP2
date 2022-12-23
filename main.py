import json

from flask import Flask, render_template, url_for, request, redirect, jsonify
from models import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/rides'
with app.app_context():
    db = SQLAlchemy(app)


@app.route('/', methods=['POST', 'GET'])
def index():  # put application's code here
    if request.method == 'POST':
        # email = request.form.get('email')
        # firstname = request.form.get('firstname')
        # lastname = request.form.get('lastname')
        # phone = request.form.get('phone')
        # password = request.form.get('password')
        # confirm_password = request.form.get('confirm_password')
        # registration = request.get_json()
        # print(registration)
        registration_data = request.get_data()
        print(registration_data)

        return registration_data
        # user = db.session.query(Role).all()
        # db.session.commit()
    else:
        return render_template('registo.html')



if __name__ == '__main__':
    app.run(debug=True)
