from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from models.profile import Profile
from models.reservation import Reservation
from models.ride import Ride

reservations = Blueprint('reservations', __name__, template_folder='templates')

@reservations.route('/reservation/<ride_id>', methods=['POST'])
@login_required
def reservation(ride_id):
    Reservation.create_reservation(Reservation(user_id=current_user.id, ride_id=int(ride_id)))
    Ride.remove_available_seat(ride_id)
    return "reserva concluida"

@reservations.route('/minhasReservas', methods=['GET'])
@login_required
def minhasReservas():
    profile = Profile.get_profile(current_user.id)
    reservas = Reservation.get_active_reservations(current_user.id)
    historicos = Reservation.get_historic_reservations(current_user.id)
    return render_template('minhasReservas.html', profile=profile, reservas=reservas, historicos=historicos)

@reservations.route('/cancel/reservation/<ride_id>', methods=['POST'])
@login_required
def cancelReservation(ride_id):
    Reservation.cancel_reservation(ride_id, current_user.id)
    Ride.add_available_seat(ride_id)
    return redirect('/minhasReservas')

@reservations.route('/getReservationCancelationModal/<ride_id>', methods=['GET'])
@login_required
def getReservationCancelationModal(ride_id):
    reservation = Reservation.get_reservation_by_user_id_and_ride_id(current_user.id, ride_id)
    ride = Ride.get_ride_by_id(ride_id)
    return render_template('reservationCancelationModal.html', reservation=reservation, ride=ride)

@reservations.route('/removePassenger/<ride_id>/<passenger_id>', methods=['PATCH'])
@login_required
def removePassenger(ride_id, passenger_id):
    Reservation.remove_passenger(passenger_id, ride_id)
    Ride.add_available_seat(ride_id)
    return redirect('/minhasBoleias')
