from flask import url_for
from flask_mail import Message, Mail

from models.ride import Ride

mail = Mail()


def sendRecoverPasswordEmail(user):
    token = user.get_reset_token()
    msg = Message(
        'Recuperação de Password - Boleias ISMAT',
        sender='boleiasismat@gmail.com',
        recipients=[user.email]
    )
    msg.body = f'''Para recuperar a sua password, entre no seguinte link:
    {url_for('auth.reset_token', token=token, _external=True)}

    Se não foi você que fez o pedido de recuperação ignore este email.
    '''
    mail.send(msg)


def sendRatingEmail(ride_id):
    passengers = Ride.get_ride_passengers(ride_id)
    ride = Ride.get_ride_by_id(ride_id)
    for passenger in passengers:
        token = 'a'
        msg = Message(
            'Avalie a sua boleia - Boleias ISMAT',
            sender='boleiasismat@gmail.com',
            recipients=[passenger.email]
        )
        msg.body = f'''Para avaliar a boleia {ride.origin.upper()} - {ride.destination.upper()} no dia {ride.ride_date} às {ride.ride_hour}, entre no seguinte link:
        {url_for('ratings.send_rating_token', token=token, _external=True)}

        Se não foi você que participou nesta boleia ignore este email.
        '''
        mail.send(msg)
