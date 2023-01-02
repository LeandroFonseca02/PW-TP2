import re
from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user

from models.profile import Profile
from models.ride import Ride
from models.user import User
from models.vehicle import Vehicle

rides = Blueprint('rides', __name__, template_folder='templates')

@rides.route('/createRide', methods=['POST'])
@login_required
def create_ride():
    if request.method == 'POST':
        car = request.form.get('car')
        origin = request.form.get('origin')
        destination = request.form.get('destination')
        date = request.form.get('date')
        hour = request.form.get('hour')
        description = request.form.get('description')
        available_seats = request.form.get('availableSeats')
        license_plate = re.findall(r"(?<=\()(.*?)(?=\))", car)
        vehicle_id = Vehicle.get_vehicle_id_by_license_plate(license_plate[0])
        Ride.create_ride(Ride(vehicle_id=vehicle_id, user_id=current_user.id, ride_date=date, ride_hour=hour,
                        number_of_available_seats=available_seats, origin=origin, destination=destination, description=description))
        return redirect('/')

@rides.route('/getRideData/<ride_id>/<card_type>', methods=['GET'])
@login_required
def getRideData(ride_id, card_type):
    passengers = Ride.get_ride_passengers(ride_id)
    ride = Ride.get_ride_by_id(ride_id)
    vehicle = Vehicle.get_vehicle_by_id(ride.vehicle_id)
    return render_template('card-content.html', passengers=passengers, ride=ride, vehicle=vehicle, card_type=card_type)

@rides.route('/minhasBoleias', methods=['GET'])
@login_required
def minhasBoleias():
    profile = Profile.get_profile(current_user.id)
    boleias = Ride.get_active_rides(current_user.id)
    historicos = Ride.get_historic_rides(current_user.id)

    return render_template('minhasBoleias.html', profile=profile, boleias=boleias, historicos=historicos)


@rides.route('/searchRide', methods=['POST'])
@login_required
def searchRide():
    filters=''
    form = request.form
    origin = form.get('inputOrigem')
    destination = form.get('inputDestino')
    ride_date = form.get('inputData')
    ride_hour = form.get('inputHora')
    if origin != '':
        filters += " AND origin = "+"'"+origin+"'"
    if destination != '':
        filters += " AND destination = "+"'"+destination+"'"
    if ride_date != '':
        filters += " AND ride_date = "+"'"+ride_date+"'"
    if ride_hour != '':
        filters += " AND ride_hour = "+"'"+ride_hour+"'"
    filteredRides = Ride.get_filtered_rides(current_user.id, filters)
    return render_template('index.html', rides=filteredRides, profile=Profile.get_profile(current_user.id))

@rides.route('/confirmRide/<ride_id>', methods=['POST'])
@login_required
def confirmRide(ride_id):
    Ride.confirm_ride(ride_id)
    return redirect('/minhasBoleias')

@rides.route('/cancelRide/<ride_id>', methods=['POST'])
@login_required
def cancelRide(ride_id):
    Ride.cancel_ride(ride_id)
    return redirect('/minhasBoleias')

@rides.route('/finalizeRide/<ride_id>', methods=['POST'])
@login_required
def finalizeRide(ride_id):
    Ride.finalize_ride(ride_id)
    return redirect('/minhasBoleias')


@rides.route('/getRideConfirmationModal/<ride_id>', methods=['GET'])
@login_required
def getRideConfirmationModal(ride_id):
    ride = Ride.get_ride_by_id(ride_id)
    return render_template('rideConfirmationModal.html', ride=ride)


@rides.route('/getRideFinalizeModal/<ride_id>', methods=['GET'])
@login_required
def getRideFinalizeModal(ride_id):
    ride = Ride.get_ride_by_id(ride_id)
    return render_template('rideFinalizeModal.html', ride=ride)

@rides.route('/getRideCancelationModal/<ride_id>', methods=['GET'])
@login_required
def getRideCancelationModal(ride_id):
    ride = Ride.get_ride_by_id(ride_id)
    return render_template('rideCancelationModal.html', ride=ride)

@rides.route('/getRideReservationModal/<ride_id>', methods=['GET'])
@login_required
def getRideReservationModal(ride_id):
    ride = Ride.get_ride_by_id(ride_id)
    return render_template('rideReservationModal.html', ride=ride)

@rides.route('/getRemovePassengerModal/<ride_id>/<passenger_id>', methods=['GET'])
@login_required
def getRemovePassengerModal(ride_id, passenger_id):
    ride = Ride.get_ride_by_id(ride_id)
    passenger = User.get_user_by_id(passenger_id)
    return render_template('passengerRemovalModal.html', ride=ride, passenger=passenger)