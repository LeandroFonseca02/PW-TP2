from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from models.profile import Profile
from models.reservation import Reservation

reservations = Blueprint('reservations', __name__, template_folder='templates')

@reservations.route('/reservation/<ride_id>', methods=['POST'])
@login_required
def reservation(ride_id):
    Reservation.create_reservation(Reservation(user_id=current_user.id, ride_id=int(ride_id)))
    return "reserva concluida"

@reservations.route('/minhasReservas', methods=['GET'])
@login_required
def minhasReservas():
    profile = Profile.get_profile(current_user.id)
    reservas = Reservation.get_active_reservations(current_user.id)
    historicos = Reservation.get_historic_reservations(current_user.id)
    return render_template('minhasReservas.html', profile=profile, reservas=reservas, historicos=historicos)

@login_required
@reservations.route('/cancel/reservation/<ride_id>', methods=['POST'])
def cancelReservation(ride_id):
    Reservation.cancel_reservation(ride_id, current_user.id)
    return redirect('/minhasReservas')