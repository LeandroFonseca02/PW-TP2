import flask
import flask_sqlalchemy
from sqlalchemy.orm import backref
from datetime import datetime
from flask_security import (RoleMixin, UserMixin)
from dataclasses import dataclass


app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/rides'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app)


roles_users_table = db.Table(
    "role_user",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


@dataclass
class User(db.Model, UserMixin):
    id: int
    email: str
    password: str
    active: bool
    roles: str

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.Unicode(255))
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship(
        "Role", secondary=roles_users_table, backref="user", lazy=True
    )

    def has_role(self, role):
        query = db.session.query(Role).filter(Role.name == role).first()
        if query:
            if query.name in self.roles:
                return True
        return False

    def __str__(self):
        return self.email

    def __repr__(self):
        return "<User %r>" % self.email

    # def __init__(self, email, password, active):
    #     self.email = email
    #     self.password = password
    #     self.active = active
    #

@dataclass
class Role(db.Model, RoleMixin):
    id: int
    name: str
    description: str

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __init__(self, name, description):
        self.name = name
        self.description = description


@dataclass
class Profile(db.Model):
    id: int
    user_id: int
    first_name: str
    last_name: str
    registration_date: str
    photo: str
    phone_number: str
    classification: float

    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey('user.id'), unique=True)
    user = db.relationship('User', backref='profile')
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    registration_date = db.Column(db.DateTime, default=datetime.now)
    photo = db.Column(db.String(60), default='../static/images/icons/profile-icon.svg')
    phone_number = db.Column(db.String(30), unique=True)
    classification = db.Column(db.Float(), db.CheckConstraint('classification >= 1 AND classification <= 5'),
                               default=2.5)

    def __str__(self):
        return self.first_name

    # def __init__(self, user_id, first_name, last_name, registration_date, photo, phone_number, classification):
    #     self.user_id = user_id
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.registration_date = registration_date
    #     self.photo = photo
    #     self.phone_number = phone_number
    #     self.classification = classification


@dataclass
class Vehicle(db.Model):
    id: int
    user_id: int
    license_plate: str
    color: str
    is_deleted: bool
    brand: str
    model: str
    created_at: str
    updated_at: str

    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey('user.id'))
    user = db.relationship('User', backref='vehicle')
    license_plate = db.Column(db.String(20), unique=True)
    color = db.Column(db.String(20))
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    # def __init__(self, user_id, license_plate, color, is_deleted, brand, model, created_at, updated_at):
    #     self.user_id = user_id
    #     self.license_plate = license_plate
    #     self.color = color
    #     self.is_deleted = is_deleted
    #     self.brand = brand
    #     self.model = model
    #     self.created_at = created_at
    #     self.updated_at = updated_at


@dataclass
class Ride(db.Model):
    id: int
    user_id: int
    vehicle_id: int
    ride_date: str
    number_of_available_seats: int
    status: str
    origin: str
    destination: str
    created_at: str
    updated_at: str

    __tablename__ = 'ride'
    __table_args__ = (db.UniqueConstraint('user_id', 'vehicle_id', 'ride_date'),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey('user.id'))
    user = db.relationship('User', backref='ride')
    vehicle_id = db.Column('vehicle_id', db.ForeignKey('vehicle.id'))
    vehicle = db.relationship('Vehicle', backref='ride')
    ride_date = db.Column(db.DateTime)
    number_of_available_seats = db.Column(db.Integer())
    status = db.Column(db.String(50), default='Aberta')
    origin = db.Column(db.String(50))
    destination = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    # def __init__(self, user_id, vehicle_id, ride_date, number_of_available_seats, status, origin, destination,
    #              created_at, updated_at):
    #     self.user_id = user_id
    #     self.vehicle_id = vehicle_id
    #     self.ride_date = ride_date
    #     self.number_of_available_seats = number_of_available_seats
    #     self.status = status
    #     self.origin = origin
    #     self.destination = destination
    #     self.created_at = created_at
    #     self.updated_at = updated_at


@dataclass
class Reservation(db.Model):
    id: int
    user_id: int
    ride_id: int
    created_at: str
    updated_at: str

    __tablename__ = 'reservation'
    __table_args__ = (db.UniqueConstraint('user_id', 'ride_id'),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey('user.id'))
    user = db.relationship('User', backref='reservation')
    ride_id = db.Column('ride_id', db.ForeignKey('ride.id'))
    ride = db.relationship('Ride', backref='reservation')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    # def __init__(self, user_id, ride_id, created_at, updated_at):
    #     self.user_id = user_id
    #     self.ride_id = ride_id
    #     self.created_at = created_at
    #     self.updated_at = updated_at


if __name__ == "__main__":
    app.app_context().push()
    db.create_all()

