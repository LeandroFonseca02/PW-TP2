import datetime
import json
from dataclasses import dataclass

import jwt

from controllers.db import db

with open('./config/config.json') as file:
    data = json.load(file)

SECRET_KEY = data['SECRET_KEY']

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

    @staticmethod
    def add_rating(ride_id, user_id, passenger_id, rating):
        db.session.add(Rating(user_id=user_id, ride_id=ride_id, passenger_id=passenger_id, rating=rating,
                              created_at=datetime.datetime.utcnow()))
        db.session.commit()


    @staticmethod
    def get_rating_token(user_id, ride_id):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            'user_id': user_id,
            'ride_id': ride_id
        }
        encoded_jwt = jwt.encode(
            payload,
            str(SECRET_KEY),
            algorithm='HS256'
        )

        return encoded_jwt

    @staticmethod
    def verify_rating_token(token):
        try:
            jwt_token = jwt.decode(
                token,
                str(SECRET_KEY),
                leeway=datetime.timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return None

        return {"user_id": jwt_token.get('user_id'), "ride_id": jwt_token.get('ride_id')}


    @staticmethod
    def check_ratings_exist(user_id, ride_id):
        ratings = db.session.query(Rating).filter(Rating.user_id == int(user_id), Rating.ride_id == int(ride_id)).all()
        if len(ratings) == 0:
            return False
        return True
