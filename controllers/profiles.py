import os
from flask import Blueprint, request, redirect, render_template, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.profile import Profile
from models.ride import Ride
from models.user import User

UPLOAD_FOLDER = './static/images/profilePictures/'


profiles  = Blueprint('profiles', __name__, template_folder='templates')

@profiles.route('/profile', methods=['GET'])
@login_required
def profile():
    profile = Profile.get_profile(current_user.id)
    return render_template('perfil.html', email=current_user.email, profile=profile)

@profiles.route('/uploadImage', methods=['POST'])
@login_required
def uploadImage():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, filename))
        Profile.update_photo(current_user.id, UPLOAD_FOLDER + filename)
        return redirect("/profile")

@profiles.route('/updateProfileData', methods=['POST'])
@login_required
def updateProfileData():  # put application's code here
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone = request.form.get('phone')
        User.update_email(current_user.id, email)
        Profile.update_name_phone(current_user.id,firstname,lastname,phone)
        return redirect("/profile")


@profiles.route('/getRideRating/<ride_id>', methods=['GET'])
@login_required
def getPassengersRating(ride_id):
    passengers = Ride.get_ride_passengers(ride_id)
    dict = {
        "ride_id": ride_id,
        "passengers":[]
    }
    for passenger in passengers:
        dict['passengers'].append({'passenger_id': passenger[0], 'passenger_classification': passenger[6]})

    return jsonify(dict)

@profiles.route('/getProfileModal/<user_id>', methods=['GET'])
@login_required
def getProfileModal(user_id):
    user = User.get_user_by_id(user_id)
    profile = Profile.get_profile(user_id)

    return render_template('profile-modal.html',email=user.email,profile=profile)

@profiles.route('/getUserRating/<user_id>', methods=['GET'])
@login_required
def getUserRating(user_id):
    profile = Profile.get_profile(user_id)
    return jsonify(rating=profile.classification)
