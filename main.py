import json

from flask import Flask, render_template
from flask_login import login_required, current_user

from controllers.profiles import profiles
from controllers.ratings import ratings
from controllers.reservations import reservations
from controllers.rides import rides
from controllers.vehicles import vehicles
from controllers.users import users
from controllers.auth import auth, login_manager
from controllers.db import db
from forms import SearchRideForm, CreateRideForm
from models.profile import Profile
from models.ride import Ride
from models.vehicle import Vehicle
from utils import mail

app = Flask(__name__)

with open('./config/config.json') as file:
    data = json.load(file)


app.config['SQLALCHEMY_DATABASE_URI'] = data['database']['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = data['database']['SQLALCHEMY_TRACK_MODIFICATIONS']
app.config['UPLOAD_FOLDER'] = data['UPLOAD_FOLDER']
app.config['SECRET_KEY'] = data['SECRET_KEY']
app.config['MAIL_SERVER'] = data['mail']['MAIL_SERVER']
app.config['MAIL_PORT'] = data['mail']['MAIL_PORT']
app.config['MAIL_USERNAME'] = data['mail']['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = data['mail']['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = data['mail']['MAIL_USE_TLS']
app.config['MAIL_USE_SSL'] = data['mail']['MAIL_USE_SSL']
mail.init_app(app)

login_manager.init_app(app)

with app.app_context():
    db.init_app(app)


@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    create_form = CreateRideForm(destination='ISMAT')
    search_form = SearchRideForm(inputDestino='ISMAT')
    rides = Ride.get_index_rides(current_user.id)
    profile = Profile.get_profile(current_user.id)
    vehicles = Vehicle.get_vehicles_by_userid(current_user.id)
    return render_template('index.html', profile=profile, title='Boleias ISMAT', rides=rides, vehicles=vehicles, search_form=search_form, create_form=create_form)


app.register_blueprint(auth)
app.register_blueprint(users)
app.register_blueprint(profiles)
app.register_blueprint(vehicles)
app.register_blueprint(rides)
app.register_blueprint(reservations)
app.register_blueprint(ratings)

if __name__ == '__main__':
    app.run(debug=True)
