import json
import flask
from controllers.db import db
from models.user import User
from models.profile import Profile
from models.role import Role
from models.vehicle import Vehicle
from models.ride import Ride
from models.reservation import Reservation
from models.rating import Rating

# MUDAR CAMINHO DO CONFIG.JSON NOS FICHEIROS models.user E models.rating
# PARA ../config/config.json
# APOS CORRER O initdb VOLTAR A COLOCAR PARA ./config/config.json

app = flask.Flask(__name__)
with open('config.json') as file:
    data = json.load(file)

app.config['SQLALCHEMY_DATABASE_URI'] = data['database']['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = data['database']['SQLALCHEMY_TRACK_MODIFICATIONS']
db.init_app(app)

if __name__ == "__main__":
    app.app_context().push()
    db.create_all()
