import datetime
from dataclasses import dataclass

from controllers.db import db


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
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    @staticmethod
    def get_vehicles_by_userid(user_id):
        return db.session.query(Vehicle).filter(Vehicle.user_id == user_id, Vehicle.is_deleted == False).all()

    @staticmethod
    def get_vehicle_by_id(id):
        return db.session.query(Vehicle).filter(Vehicle.id == id, Vehicle.is_deleted == False).first()

    @staticmethod
    def create_vehicle(user_id, brand, model, color, license_plate):
        vehicle = Vehicle(user_id=user_id, license_plate=license_plate, color=color, brand=brand, model=model)
        db.session.add(vehicle)
        db.session.commit()

    @staticmethod
    def delete_vehicle(vehicle_id):
        vehicle = Vehicle.get_vehicle_by_id(int(vehicle_id))
        vehicle.is_deleted = True
        db.session.commit()

    @staticmethod
    def get_vehicle_id_by_license_plate(license_plate):
        vehicle = db.session.query(Vehicle).filter(Vehicle.license_plate == license_plate).first()
        return vehicle.id

    # def __init__(self, user_id, license_plate, color, is_deleted, brand, model, created_at, updated_at):
    #     self.user_id = user_id
    #     self.license_plate = license_plate
    #     self.color = color
    #     self.is_deleted = is_deleted
    #     self.brand = brand
    #     self.model = model
    #     self.created_at = created_at
    #     self.updated_at = updated_at
