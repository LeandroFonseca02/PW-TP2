import datetime
from dataclasses import dataclass

from controllers.db import db
from models.reservation import Reservation
from utils import sendRatingEmail


@dataclass
class Ride(db.Model):
    id: int
    user_id: int
    vehicle_id: int
    ride_date: str
    ride_hour: str
    number_of_available_seats: int
    status: str
    origin: str
    destination: str
    description: str
    created_at: str
    updated_at: str

    __tablename__ = 'ride'
    __table_args__ = (db.UniqueConstraint('user_id', 'vehicle_id', 'ride_date', 'ride_hour'),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey('user.id'))
    user = db.relationship('User', backref='ride')
    vehicle_id = db.Column('vehicle_id', db.ForeignKey('vehicle.id'))
    vehicle = db.relationship('Vehicle', backref='ride')
    ride_date = db.Column(db.Date)
    ride_hour = db.Column(db.Time)
    number_of_available_seats = db.Column(db.Integer())
    status = db.Column(db.String(50), default='Aberta')
    origin = db.Column(db.String(50))
    destination = db.Column(db.String(50))
    description = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)

    @staticmethod
    def get_index_rides(user_id):
        query = """
        
        SELECT DISTINCT r.id,
                        rs.user_id,
                        to_char(r.ride_date, 'MM') AS ride_date_month,
                        to_char(r.ride_date, 'DD') AS ride_date_day,
                        to_char(r.ride_hour, 'HH24') AS ride_hours,
                        to_char(r.ride_hour, 'MI') AS ride_minutes,
                        r.number_of_available_seats,
                        r.status,
                        r.origin,
                        r.destination,
                        rs.is_driver
        FROM ride AS r,reservation rs
        WHERE r.status = 'Aberta'
          AND rs.ride_id = r.id
          AND rs.is_driver = TRUE
          AND r.id NOT IN (
                SELECT DISTINCT r.id
                FROM ride AS r
                    INNER JOIN reservation rs ON r.id = rs.ride_id
                WHERE rs.user_id =""" + str(user_id) + """)"""

        return db.session.execute(query).all()


    @staticmethod
    def get_ride_passengers(ride_id):
        query = """
        SELECT u.id AS user_id,
        email,
        first_name,
        last_name,
        photo,
        phone_number,
        classification,
        is_driver,
        r.created_at
        FROM "user" AS u
             JOIN profile p ON u.id = p.user_id
             JOIN reservation r ON u.id = r.user_id
             JOIN ride r2 ON r2.id = r.ride_id
        WHERE (r.status != 'Cancelada' OR is_driver = true) AND r2.id =
        """ + str(ride_id) + """ ORDER BY r.created_at ASC"""

        return db.session.execute(query).all()

    @staticmethod
    def get_ride_by_id(ride_id):
        return db.session.query(Ride).filter(Ride.id == int(ride_id)).first()

    @staticmethod
    def create_ride(ride):
        db.session.add(ride)
        db.session.commit()
        Reservation.create_reservation(Reservation(user_id=ride.user_id, ride_id=ride.id, is_driver=True))


    @staticmethod
    def get_active_rides(user_id):
        query = """
            SELECT r.id,
               r.user_id,
               to_char(r.ride_date, 'MM') AS ride_date_month,
               to_char(r.ride_date, 'DD') AS ride_date_day,
               to_char(r.ride_hour, 'HH24') AS ride_hours,
               to_char(r.ride_hour, 'MI') AS ride_minutes,
               r.number_of_available_seats,
               r.status,
               r.origin,
               r.destination
            FROM ride AS r
            WHERE (r.status = 'Aberta' OR r.status = 'Confirmada')
            AND r.user_id =""" + str(user_id)
        return db.session.execute(query).all()


    @staticmethod
    def get_historic_rides(user_id):
        query = """
            SELECT r.id,
               r.user_id,
               to_char(r.ride_date, 'MM') AS ride_date_month,
               to_char(r.ride_date, 'DD') AS ride_date_day,
               to_char(r.ride_hour, 'HH24') AS ride_hours,
               to_char(r.ride_hour, 'MI') AS ride_minutes,
               r.number_of_available_seats,
               r.status,
               r.origin,
               r.destination
            FROM ride AS r
            WHERE (r.status = 'Concluida' OR r.status = 'Cancelada')
              AND r.user_id =""" + str(user_id)
        return db.session.execute(query).all()

    @staticmethod
    def get_filtered_rides(user_id,  filters):
        query = """ 
                SELECT DISTINCT r.id,
                                rs.user_id,
                                to_char(r.ride_date, 'MM') AS ride_date_month,
                                to_char(r.ride_date, 'DD') AS ride_date_day,
                                to_char(r.ride_hour, 'HH24') AS ride_hours,
                                to_char(r.ride_hour, 'MI') AS ride_minutes,
                                r.number_of_available_seats,
                                r.status,
                                r.origin,
                                r.destination,
                                rs.is_driver
                FROM ride AS r,reservation rs
                WHERE r.status = 'Aberta'
                  AND rs.ride_id = r.id
                  AND rs.is_driver = TRUE
                  AND r.id NOT IN (
                        SELECT DISTINCT r.id
                        FROM ride AS r
                            INNER JOIN reservation rs ON r.id = rs.ride_id
                        WHERE rs.user_id =""" + str(user_id) + """)"""+filters
        return db.session.execute(query).all()


    @staticmethod
    def confirm_ride(ride_id):
        ride = Ride.get_ride_by_id(int(ride_id))
        ride.status = 'Confirmada'
        reservations = Reservation.get_reservations_by_ride_id(ride_id)
        for reservation in reservations:
            reservation.status = 'Confirmada'
        db.session.commit()
        sendRatingEmail(Ride.get_ride_by_id(ride_id), Ride.get_ride_passengers(ride_id))

    @staticmethod
    def cancel_ride(ride_id):
        ride = Ride.get_ride_by_id(int(ride_id))
        ride.status = 'Cancelada'
        reservations = Reservation.get_reservations_by_ride_id(ride_id)
        for reservation in reservations:
            reservation.status = 'Cancelada'
        db.session.commit()

    @staticmethod
    def finalize_ride(ride_id):
        ride = Ride.get_ride_by_id(int(ride_id))
        ride.status = 'Concluida'
        reservations = Reservation.get_reservations_by_ride_id(ride_id)
        for reservation in reservations:
            reservation.status = 'Concluida'
        db.session.commit()

    @staticmethod
    def remove_available_seat(ride_id):
        ride = Ride.get_ride_by_id(int(ride_id))
        ride.number_of_available_seats += -1
        db.session.commit()

    @staticmethod
    def add_available_seat(ride_id):
        ride = Ride.get_ride_by_id(int(ride_id))
        ride.number_of_available_seats += 1
        db.session.commit()
