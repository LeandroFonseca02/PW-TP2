import re
from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user

from models.ride import Ride
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
