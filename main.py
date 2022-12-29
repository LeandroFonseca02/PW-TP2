from flask import Flask, url_for, render_template
from flask_login import login_required, current_user
from flask_mail import Mail, Message

from controllers.profiles import UPLOAD_FOLDER, profiles
from controllers.rides import rides
from controllers.vehicles import vehicles
from controllers.users import users
from controllers.auth import auth, login_manager
from controllers.db import db
from models.profile import Profile
from models.ride import Ride
from models.vehicle import Vehicle

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/rides'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'secret'



app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'boleiasismat@gmail.com'
app.config['MAIL_PASSWORD'] = 'irawvczpnfosintg'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


login_manager.init_app(app)


with app.app_context():
    db.init_app(app)

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
def index():
    rides = Ride.get_index_rides(current_user.id)
    profile = Profile.get_profile(current_user.id)
    vehicles = Vehicle.get_vehicles_by_userid(current_user.id)
    return render_template('index.html', profile=profile, title='Boleias ISMAT', rides=rides, vehicles=vehicles)







#
#
# @app.route('/reservation/<ride_id>', methods=['POST'])
# @login_required
# def reservation(ride_id):
#     new_reservation = Reservation(user_id=current_user.id, ride_id=int(ride_id))
#     db.session.add(new_reservation)
#     db.session.commit()
#     return "reserva concluida"
#
#
# @app.route('/minhasBoleias', methods=['GET'])
# @login_required
# def minhasBoleias():
#     profile = db.session.query(Profile).filter(Profile.user_id == current_user.id).first()
#
#     boleias = db.session.execute("""
#     SELECT r.id,
#        r.user_id,
#        to_char(r.ride_date, 'MM') AS ride_date_month,
#        to_char(r.ride_date, 'DD') AS ride_date_day,
#        to_char(r.ride_hour, 'HH') AS ride_hours,
#        to_char(r.ride_hour, 'MI') AS ride_minutes,
#        r.number_of_available_seats,
#        r.status,
#        r.origin,
#        r.destination
#     FROM ride AS r
#     WHERE (r.status = 'Aberta' OR r.status = 'Confirmada')
#     AND r.user_id =""" + str(current_user.id)).all()
#
#     historicos = db.session.execute("""
#     SELECT r.id,
#        r.user_id,
#        to_char(r.ride_date, 'MM') AS ride_date_month,
#        to_char(r.ride_date, 'DD') AS ride_date_day,
#        to_char(r.ride_hour, 'HH') AS ride_hours,
#        to_char(r.ride_hour, 'MI') AS ride_minutes,
#        r.number_of_available_seats,
#        r.status,
#        r.origin,
#        r.destination
#     FROM ride AS r
#     WHERE (r.status = 'Concluida' OR r.status = 'Cancelada')
#       AND r.user_id =""" + str(current_user.id)).all()
#
#     return render_template('minhasBoleias.html', profile=profile, boleias=boleias, historicos=historicos)
#
#
# @app.route('/minhasReservas', methods=['GET'])
# @login_required
# def minhasReservas():
#     profile = db.session.query(Profile).filter(Profile.user_id == current_user.id).first()
#     reservas = db.session.execute("""
#     SELECT r.id,
#        r.user_id,
#        to_char(r.ride_date, 'MM') AS ride_date_month,
#        to_char(r.ride_date, 'DD') AS ride_date_day,
#        to_char(r.ride_hour, 'HH') AS ride_hours,
#        to_char(r.ride_hour, 'MI') AS ride_minutes,
#        r.number_of_available_seats,
#        rs.status,
#        r.origin,
#        r.destination
#     FROM ride AS r,
#          reservation AS rs
#     WHERE (rs.status = 'Aberta' OR rs.status = 'Confirmada')
#       AND rs.ride_id = r.id
#       AND rs.is_driver = FALSE
#       AND rs.user_id = """ + str(current_user.id)).all()
#
#     historicos = db.session.execute("""
#     SELECT r.id,
#        r.user_id,
#        to_char(r.ride_date, 'MM') AS ride_date_month,
#        to_char(r.ride_date, 'DD') AS ride_date_day,
#        to_char(r.ride_hour, 'HH') AS ride_hours,
#        to_char(r.ride_hour, 'MI') AS ride_minutes,
#        r.number_of_available_seats,
#        rs.status,
#        r.origin,
#        r.destination
#     FROM ride AS r,
#          reservation AS rs
#     WHERE (rs.status = 'Concluida' OR rs.status = 'Cancelada')
#       AND rs.ride_id = r.id
#       AND rs.is_driver = FALSE
#       AND rs.user_id =""" + str(current_user.id)).all()
#
#     return render_template('minhasReservas.html', profile=profile, reservas=reservas, historicos=historicos)
#
#
# @app.route('/reset_password', methods=['GET', 'POST'])
# def reset_request():
#     if current_user.is_authenticated:
#         return redirect('/')
#     form = RequestResetForm()
#     if form.is_submitted():
#         user = db.session.query(User).filter(User.email == form.email.data).first()
#         sendRecoverPasswordEmail(user)
#         return redirect('/login')
#     return render_template('reset_request.html', form=form)
#
#
# @app.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_token(token):
#     if current_user.is_authenticated:
#         return redirect('/')
#     user_id = User.verify_reset_token(token)
#     if user_id is None:
#         print('Token inválido ou expirado')
#         return redirect('/reset_password')
#     form = ResetPasswordForm()
#
#     if form.is_submitted():
#         password = form.password.data
#         confirm_password = form.confirm_password.data
#         if password != confirm_password:
#             return "Passwords diferentes"
#         else:
#             user = db.session.query(User).filter(User.id == user_id).first()
#             user.password = generate_password_hash(password, method='sha256')
#             db.session.commit()
#
#             return redirect('/login')
#
#     return render_template('reset_token.html', form=form)
#
#
# @login_required
# @app.route('/cancel/reservation/<ride_id>', methods=['POST'])
# def cancelReservation(ride_id):
#     reservation = db.session.query(Reservation).filter(Reservation.ride_id == int(ride_id), Reservation.user_id == current_user.id).first()
#     reservation.status = 'Cancelada'
#     db.session.commit()
#     return redirect('/minhasReservas')

app.register_blueprint(auth)
app.register_blueprint(users)
app.register_blueprint(profiles)
app.register_blueprint(vehicles)
app.register_blueprint(rides)



if __name__ == '__main__':
    app.run(debug=True)
