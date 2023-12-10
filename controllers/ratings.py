from flask import Blueprint, redirect, render_template, request
from flask_login import current_user, login_required

from models.profile import Profile
from models.rating import Rating
from models.ride import Ride

ratings = Blueprint('ratings', __name__, template_folder='templates')


@ratings.route('/rating/<token>', methods=['GET', 'POST'])
@login_required
def rating_token(token):
    data = Rating.verify_rating_token(token)
    if data is None:
        return 'Token inválido ou expirado'

    ride_id = data.get('ride_id')
    passengers = Ride.get_ride_passengers(ride_id)

    if Rating.check_ratings_exist(current_user.id, ride_id):
        return "Você já avaliou esta boleia!"
    else:
        profile = Profile.get_profile(current_user.id)
        return render_template('rating.html', passengers=passengers, user_id=current_user.id, profile=profile,
                               ride_id=ride_id)



@ratings.route('/sendRatings/<ride_id>', methods=['GET', 'POST'])
@login_required
def update_ratings(ride_id):
    form = request.form
    passengers = Ride.get_ride_passengers(ride_id)
    for passenger in passengers:
        if passenger.user_id != current_user.id:
            Rating.add_rating(int(ride_id), current_user.id, passenger.user_id, form.get(str(passenger.user_id)))
    return "Ratings adicionadas com sucesso"