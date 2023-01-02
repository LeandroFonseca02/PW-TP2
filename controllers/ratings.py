from flask import Blueprint, redirect, render_template, request
from flask_login import current_user, login_required

from forms import RatingForm
from models.profile import Profile
from models.rating import Rating
from models.ride import Ride

ratings = Blueprint('ratings', __name__, template_folder='templates')

@ratings.route('/')
def send_rating_email():
    return ""


@ratings.route('/send_rating_token', methods=['GET', 'POST'])
@login_required
def send_rating_token():
    form = RatingForm()
    ride_id = '1'
    passengers = Ride.get_ride_passengers(ride_id)

    # user_id = User.verify_reset_token(token)
    # if user_id is None:
    #     print('Token inválido ou expirado')
    #     return redirect('/reset_password')
    # form = ResetPasswordForm()
    #
    # if form.is_submitted():
    #     password = form.password.data
    #     confirm_password = form.confirm_password.data
    #     if password != confirm_password:
    #         return "Passwords diferentes"
    #     else:
    #         User.update_password(user_id, generate_password_hash(password, method='sha256'))
    #         return redirect('/login')

    profile = Profile.get_profile(current_user.id)
    return render_template('modal-rating.html', form=form, passengers=passengers, user_id=current_user.id, profile=profile, ride_id=ride_id)



@ratings.route('/sendRatings/<ride_id>', methods=['GET', 'POST'])
@login_required
def update_ratings(ride_id):
    form = request.form
    passengers = Ride.get_ride_passengers(ride_id)
    for passenger in passengers:
        if passenger.user_id != current_user.id:
            Rating.add_rating(int(ride_id), current_user.id, passenger.user_id, form.get(str(passenger.user_id)))
    return "Ratings adicionadas com sucesso"