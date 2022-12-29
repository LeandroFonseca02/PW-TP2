from flask import Flask, url_for, render_template
from flask_login import login_required, current_user
from flask_mail import Mail, Message

from controllers.profiles import UPLOAD_FOLDER, profiles
from controllers.reservations import reservations
from controllers.rides import rides
from controllers.vehicles import vehicles
from controllers.users import users
from controllers.auth import auth, login_manager
from controllers.db import db
from models.profile import Profile
from models.ride import Ride
from models.vehicle import Vehicle
from utils import mail


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
mail.app = app


login_manager.init_app(app)


with app.app_context():
    db.init_app(app)


@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    rides = Ride.get_index_rides(current_user.id)
    profile = Profile.get_profile(current_user.id)
    vehicles = Vehicle.get_vehicles_by_userid(current_user.id)
    return render_template('index.html', profile=profile, title='Boleias ISMAT', rides=rides, vehicles=vehicles)


app.register_blueprint(auth)
app.register_blueprint(users)
app.register_blueprint(profiles)
app.register_blueprint(vehicles)
app.register_blueprint(rides)
app.register_blueprint(reservations)



if __name__ == '__main__':
    app.run(debug=True)
