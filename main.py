import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from models import *
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from forms import LoginForm, RegisterForm, RequestResetForm, ResetPasswordForm



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/rides'
UPLOAD_FOLDER = './static/images/profilePictures/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'secret'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'boleiasismat@gmail.com'
app.config['MAIL_PASSWORD'] = 'irawvczpnfosintg'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return db.session.query(User).filter(User.id == id).first()


with app.app_context():
    db = SQLAlchemy(app)

def sendRecoverPasswordEmail(user):
    token = user.get_reset_token()
    msg = Message(
    'Recuperação de Password - Boleias ISMAT',
    sender = 'boleiasismat@gmail.com',
    recipients = [user.email]
    )
    msg.body = f'''Para recuperar a sua password, entre no seguinte link:
    {url_for('reset_token',token=token, _external=True)}
    
    Se não foi você que fez o pedido de recuperação ignore este email.
    '''
    mail.send(msg)
    print("Email enviado")


@app.route('/', methods=['POST', 'GET'])
@login_required
def index():  # put application's code here
    rides = db.session.execute("""
    SELECT r.id,
        r.user_id,
        to_char(r.ride_date, 'MM') AS ride_date_month,
        to_char(r.ride_date, 'DD') AS ride_date_day,
        to_char(r.ride_hour, 'HH') AS ride_hours,
        to_char(r.ride_hour, 'MI') AS ride_minutes,
        r.number_of_available_seats,
        r.status,
        r.origin,
        r.destination
    FROM ride AS r,
        reservation AS rs
    WHERE r.status = 'Aberta'
        AND rs.ride_id = r.id
        AND rs.is_driver = FALSE
        AND r.user_id != """+str(current_user.id)+"""
        AND rs.user_id != """+str(current_user.id)).all()

    profile = db.session.query(Profile).filter(Profile.user_id == current_user.id).first()
    vehicles = db.session.query(Vehicle).filter(Vehicle.user_id == current_user.id, Vehicle.is_deleted == False).all()
    return render_template('index.html', profile=profile, title='Boleias ISMAT', rides=rides, vehicles=vehicles)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()

    if form.is_submitted():
        email = form.email.data
        password = form.password.data
        user = db.session.query(User).filter(User.email == email).first()
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


@app.route('/register', methods=['POST', 'GET'])
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
        return render_template('criar-utilizador.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/profile', methods=['GET'])
@login_required
def profile():  # put application's code here
    profile = db.session.query(Profile).filter(Profile.user_id == current_user.id).first()
    return render_template('perfil.html', email=current_user.email, profile=profile)


@app.route('/getVehicles', methods=['GET'])
@login_required
def get_vehicles():  # put application's code here
    vehicles = db.session.query(Vehicle).filter(Vehicle.user_id == current_user.id, Vehicle.is_deleted == False).all()
    return render_template('car-manager.html', vehicles=vehicles)


@app.route('/uploadImage', methods=['POST'])
@login_required
def uploadImage():  # put application's code here
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, filename))
        profile = db.session.query(Profile).filter(Profile.user_id == current_user.id).first()
        profile.photo = UPLOAD_FOLDER + filename
        print(profile.photo)
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
        return redirect('/')


@app.route('/deleteVehicle/<vehicle_id>', methods=['PATCH'])
@login_required
def delete_vehicle(vehicle_id):
    if request.method == 'PATCH':
        vehicle = db.session.query(Vehicle).filter(Vehicle.id == int(vehicle_id)).first()
        vehicle.is_deleted = True
        db.session.commit()

        return redirect('/')

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
        ride_reservation = Reservation(user_id=current_user.id,ride_id=new_ride.id,is_driver=True)
        db.session.add(ride_reservation)
        db.session.commit()

        return redirect('/')


@app.route('/getRideData/<ride_id>', methods=['GET'])
@login_required
def getRideData(ride_id):
    passengers_query = """
    SELECT u.id AS user_id,
        email,
        first_name,
        last_name,
        photo,
        phone_number,
        classification
    FROM "user" AS u
         JOIN profile p ON u.id = p.user_id
         JOIN reservation r ON u.id = r.user_id
         JOIN ride r2 ON r2.id = r.ride_id
    WHERE r2.id =""" + ride_id

    passengers = db.session.execute(passengers_query).all()
    ride = db.session.query(Ride).filter(Ride.id == int(ride_id)).first()
    vehicle = db.session.query(Vehicle).filter(Vehicle.id == ride.vehicle_id).first()
    return render_template('card-content.html', passengers=passengers, ride=ride, vehicle=vehicle)


@app.route('/getRideRating/<ride_id>', methods=['GET'])
@login_required
def getRideRating(ride_id):
    passengers_query = """
    SELECT u.id AS user_id,
        email,
        first_name,
        last_name,
        photo,
        phone_number,
        classification
    FROM "user" AS u
        JOIN profile p ON u.id = p.user_id
        JOIN reservation r ON u.id = r.user_id
        JOIN ride r2 ON r2.id = r.ride_id
    WHERE r2.id =""" + ride_id

    passengers = db.session.execute(passengers_query).all()
    dict = {
        "ride_id": ride_id,
        "passengers":[]
    }
    for passenger in passengers:
        dict['passengers'].append({'passenger_id': passenger[0], 'passenger_classification': passenger[6]})

    return jsonify(dict)


@app.route('/getProfileModal/<user_id>', methods=['GET'])
@login_required
def getProfileModal(user_id):
    user = db.session.query(User).filter(User.id == int(user_id)).first()
    profile = db.session.query(Profile).filter(Profile.user_id == int(user_id)).first()

    return render_template('profile-modal.html',email=user.email,profile=profile)

@app.route('/getUserRating/<user_id>', methods=['GET'])
@login_required
def getUserRating(user_id):
    profile = db.session.query(Profile).filter(Profile.user_id == int(user_id)).first()
    return jsonify(rating = profile.classification)


@app.route('/reservation/<ride_id>', methods=['POST'])
@login_required
def reservation(ride_id):
    new_reservation = Reservation(user_id=current_user.id, ride_id=int(ride_id))
    db.session.add(new_reservation)
    db.session.commit()
    return "reserva concluida"


@app.route('/minhasBoleias', methods=['GET'])
@login_required
def minhasBoleias():
    profile = db.session.query(Profile).filter(Profile.user_id == current_user.id).first()

    boleias = db.session.execute("""
    SELECT r.id,
       r.user_id,
       to_char(r.ride_date, 'MM') AS ride_date_month,
       to_char(r.ride_date, 'DD') AS ride_date_day,
       to_char(r.ride_hour, 'HH') AS ride_hours,
       to_char(r.ride_hour, 'MI') AS ride_minutes,
       r.number_of_available_seats,
       r.status,
       r.origin,
       r.destination
    FROM ride AS r
    WHERE (r.status = 'Aberta' OR r.status = 'Confirmada')
    AND r.user_id =""" + str(current_user.id)).all()

    historicos = db.session.execute("""
    SELECT r.id,
       r.user_id,
       to_char(r.ride_date, 'MM') AS ride_date_month,
       to_char(r.ride_date, 'DD') AS ride_date_day,
       to_char(r.ride_hour, 'HH') AS ride_hours,
       to_char(r.ride_hour, 'MI') AS ride_minutes,
       r.number_of_available_seats,
       r.status,
       r.origin,
       r.destination
    FROM ride AS r
    WHERE (r.status = 'Concluida' OR r.status = 'Cancelada')
      AND r.user_id =""" + str(current_user.id)).all()

    return render_template('minhasBoleias.html', profile=profile, boleias=boleias, historicos=historicos)


@app.route('/minhasReservas', methods=['GET'])
@login_required
def minhasReservas():
    profile = db.session.query(Profile).filter(Profile.user_id == current_user.id).first()
    reservas = db.session.execute("""
    SELECT r.id,
       r.user_id,
       to_char(r.ride_date, 'MM') AS ride_date_month,
       to_char(r.ride_date, 'DD') AS ride_date_day,
       to_char(r.ride_hour, 'HH') AS ride_hours,
       to_char(r.ride_hour, 'MI') AS ride_minutes,
       r.number_of_available_seats,
       rs.status,
       r.origin,
       r.destination
    FROM ride AS r,
         reservation AS rs
    WHERE (rs.status = 'Aberta' OR rs.status = 'Confirmada')
      AND rs.ride_id = r.id
      AND rs.is_driver = FALSE
      AND rs.user_id = """ + str(current_user.id)).all()

    historicos = db.session.execute("""
    SELECT r.id,
       r.user_id,
       to_char(r.ride_date, 'MM') AS ride_date_month,
       to_char(r.ride_date, 'DD') AS ride_date_day,
       to_char(r.ride_hour, 'HH') AS ride_hours,
       to_char(r.ride_hour, 'MI') AS ride_minutes,
       r.number_of_available_seats,
       rs.status,
       r.origin,
       r.destination
    FROM ride AS r,
         reservation AS rs
    WHERE (rs.status = 'Concluida' OR rs.status = 'Cancelada')
      AND rs.ride_id = r.id
      AND rs.is_driver = FALSE
      AND rs.user_id =""" + str(current_user.id)).all()

    return render_template('minhasReservas.html', profile=profile, reservas=reservas, historicos=historicos)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect('/')
    form = RequestResetForm()
    if form.is_submitted():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        sendRecoverPasswordEmail(user)
        return redirect('/login')
    return render_template('reset_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
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
            user = db.session.query(User).filter(User.id == user_id).first()
            user.password = generate_password_hash(password, method='sha256')
            db.session.commit()

            return redirect('/login')

    return render_template('reset_token.html', form=form)







if __name__ == '__main__':
    app.run(debug=True)
