from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from models.vehicle import Vehicle

vehicles = Blueprint('vehicles', __name__, template_folder='templates')

@vehicles.route('/getVehicles', methods=['GET'])
@login_required
def get_vehicles():
    vehicles = Vehicle.get_vehicles_by_userid(current_user.id)
    return render_template('car-manager.html', vehicles=vehicles)

@vehicles.route('/createVehicle', methods=['POST'])
@login_required
def createVehicle():  # put application's code here
    if request.method == 'POST':
        brand = request.form.get('brand')
        model = request.form.get('model')
        color = request.form.get('color')
        licensePlate = request.form.get('licensePlate')
        Vehicle.create_vehicle(current_user.id, brand, model, color, licensePlate)
        return redirect('/profile')

@vehicles.route('/deleteVehicle/<vehicle_id>', methods=['PATCH'])
@login_required
def delete_vehicle(vehicle_id):
    if request.method == 'PATCH':
        Vehicle.delete_vehicle(vehicle_id)
        return redirect('/')