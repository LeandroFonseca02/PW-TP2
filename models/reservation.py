import datetime
from dataclasses import dataclass
from controllers.db import db


@dataclass
class Reservation(db.Model):
    id: int
    user_id: int
    ride_id: int
    status: str
    is_driver: bool
    created_at: str
    updated_at: str

    __tablename__ = 'reservation'
    __table_args__ = (db.UniqueConstraint('user_id', 'ride_id'),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey('user.id'))
    user = db.relationship('User', backref='reservation')
    ride_id = db.Column('ride_id', db.ForeignKey('ride.id'))
    ride = db.relationship('Ride', backref='reservation')
    status = db.Column(db.String(50), default='Aberta')
    is_driver = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)

    @staticmethod
    def create_reservation(reservation):
        db.session.add(reservation)
        db.session.commit()

    # def __init__(self, user_id, ride_id, created_at, updated_at):
    #     self.user_id = user_id
    #     self.ride_id = ride_id
    #     self.created_at = created_at
    #     self.updated_at = updated_at
