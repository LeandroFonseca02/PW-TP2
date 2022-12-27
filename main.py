import json
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, jsonify
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from models import *
from flask_sqlalchemy import SQLAlchemy

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
    rides = db.session.execute('SELECT r.id,r.user_id,extract(MONTH FROM r.ride_date) AS ride_date_month, '
                               'extract(DAY FROM r.ride_date) AS ride_date_day,extract(HOURS FROM r.ride_hour) AS ride_hours, '
                               'extract(MINUTES FROM r.ride_hour) AS ride_minutes,r.number_of_available_seats,r.status,r.origin,r.destination '
                               'FROM ride AS r').all()
    profile = db.session.query(Profile).filter(Profile.user_id == current_user.id).first()
    vehicles = db.session.query(Vehicle).filter(Vehicle.user_id == current_user.id).all()
    return render_template('index.html', profile=profile, title='Boleias ISMAT', rides=rides, vehicles=vehicles)


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
                new_user = User(email=email, password=generate_password_hash(password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                new_profile = Profile(user_id=new_user.id, first_name=firstname, last_name=lastname, phone_number=phone)
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
    profile = db.session.query(Profile).filter(Profile.user_id == current_user.id).first()
    vehicles = db.session.query(Vehicle).filter(Vehicle.user_id == current_user.id)
    return render_template('perfil.html', email=current_user.email, profile=profile, vehicles=vehicles)


@app.route('/uploadImage', methods=['POST'])
@login_required
def uploadImage():  # put application's code here
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, filename))
        profile = db.session.query(Profile).filter(Profile.user_id == current_user.id).first()
        profile.photo = UPLOAD_FOLDER + filename
        db.session.commit()
        return redirect("/profile")


@app.route('/updateProfileData', methods=['POST'])
@login_required
def updateProfileData():  # put application's code here
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone = request.form.get('phone')
        user = db.session.query(User).filter(User.id == current_user.id).first()
        profile = db.session.query(Profile).filter(Profile.user_id == user.id).first()
        user.email = email
        profile.first_name = firstname
        profile.last_name = lastname
        profile.phone_number = phone
        db.session.commit()
        return redirect("/profile")


@app.route('/updatePassword', methods=['POST'])
@login_required
def updatePassword():  # put application's code here
    if request.method == 'POST':
        password = request.form.get('password')
        newPassword = request.form.get('newPassword')
        passwordConfirmation = request.form.get('passwordConfirmation')
        user = db.session.query(User).filter(User.id == current_user.id).first()

        if check_password_hash(user.password, password):
            if newPassword == passwordConfirmation:
                user.password = generate_password_hash(newPassword, method='sha256')
                db.session.commit()
                return redirect("/profile")
            else:
                return "password desigual"
        else:
            return "password incorreta"


@app.route('/createVehicle', methods=['POST'])
@login_required
def createVehicle():  # put application's code here
    if request.method == 'POST':
        brand = request.form.get('brand')
        model = request.form.get('model')
        color = request.form.get('color')
        licensePlate = request.form.get('licensePlate')
        new_vehicle = Vehicle(user_id=current_user.id, license_plate=licensePlate, color=color,
                              brand=brand, model=model)
        db.session.add(new_vehicle)
        db.session.commit()
        return "sucesso"


@app.route('/createRide', methods=['POST'])
@login_required
def create_ride():
    if request.method == 'POST':
        car = request.form.get('car')
        origin = request.form.get('origin')
        destination = request.form.get('destination')
        date = request.form.get('date')
        hour = request.form.get('hour')
        description = request.form.get('description')
        available_seats = request.form.get('availableSeats')
        new_ride = Ride(vehicle_id=1, user_id=current_user.id, ride_date=date, ride_hour=hour,
                        number_of_available_seats=available_seats, origin=origin, destination=destination, description=description)
        db.session.add(new_ride)
        db.session.commit()
        return redirect('/')


@app.route('/getRideData/<ride_id>', methods=['GET'])
@login_required
def getRideData(ride_id):
    passengers_query = """
        select u.id as user_id, email, first_name, last_name,
            photo, phone_number, classification
            from "user" as u join profile p on u.id = p.user_id
            join reservation r on u.id = r.user_id join ride r2 on r2.id = r.ride_id
            where r2.id = """ + ride_id
    condutor_query = """SELECT  u.id as user_id, email, first_name, last_name,
        photo, phone_number, classification FROM "user" as u, profile p , ride r
        WHERE u.id = p.user_id AND r.user_id = u.id AND r.id = """ + ride_id
    condutor = db.session.execute(condutor_query).first()
    passengers = db.session.execute(passengers_query).all()
    ride = db.session.query(Ride).filter(Ride.id == int(ride_id)).first()
    vehicle = db.session.query(Vehicle).filter(Vehicle.id == ride.vehicle_id).first()
    return render_template('card-content.html', passengers=passengers, ride=ride, condutor=condutor, vehicle=vehicle)


@app.route('/getRideRating/<ride_id>', methods=['GET'])
@login_required
def getRideRating(ride_id):
    passengers_query = """
        select u.id as user_id, email, first_name, last_name,
            photo, phone_number, classification
            from "user" as u join profile p on u.id = p.user_id
            join reservation r on u.id = r.user_id join ride r2 on r2.id = r.ride_id
            where r2.id = """ + ride_id
    condutor_query = """SELECT  u.id as user_id, email, first_name, last_name,
        photo, phone_number, classification FROM "user" as u, profile p , ride r
        WHERE u.id = p.user_id AND r.user_id = u.id AND r.id = """ + ride_id
    condutor = db.session.execute(condutor_query).first()
    passengers = db.session.execute(passengers_query).all()
    ride = db.session.query(Ride).filter(Ride.id == int(ride_id)).first()
    dict = {
        "ride_id": ride.id,
        "condutor_id": condutor[0],
        "condutor_classification": condutor[6],
        "passengers":[]
    }
    for passenger in passengers:
        dict['passengers'].append({'passenger_id': passenger[0], 'passenger_classification': passenger[6]})

    return jsonify(dict)


if __name__ == '__main__':
    app.run(debug=True)
