from flask import url_for
from flask_mail import Message, Mail

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


# def sendRatingEmail(ride, passengers):
    # for passenger in passengers:
        # token =