from dataclasses import dataclass
from controllers.db import db


@dataclass
class Rating(db.Model):
    id: int
    user_id: int
    ride_id: int
    passenger_id: int
    rating: int
    created_at: str
    updated_at: str

    __tablename__ = 'rating'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    ride_id = db.Column(db.Integer)
    passenger_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
