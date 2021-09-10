import sendgrid
from django.template.loader import get_template
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from sendgrid import Email, To, Content, Mail
from django.core.mail import send_mail

from mysite.helpers.tokens import account_token
from mysite import settings 

sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

# send_mail("Subject", "text body", "from@example.com",
#           ["to@example.com"], html_message="<html>html body</html>")

def send_welcome(user, domain):
    """
    Sends a welcome verification email to a user

    Args:
        user (webapp.models.User): The receiver User object
        domain (str): The site's domain

    Returns:
        bool: a boolean value representing success status
    """

    user_email = user.email
    first_name = user.first_name
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_token.make_token(user)

    verification_url = f'{domain}/verify-email?uid={uid}&token={token}'

    data = {
        'first_name': first_name,
        'verification_url': verification_url
    }

    from_email = Email('welcome@etsea.com')
    to_email = To(user_email)
    subject = 'Welcome to Etsea 🚀'
    html_content = get_template('welcome.html').render(data)
    content = Content('text/html', html_content)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)

    return True


def send_email_verification(user, domain):
    """
    Sends a verification email to a user

    Args:
        user (webapp.models.User): The receiver User object
        domain (str): The site's domain

    Returns:
        bool: a boolean value representing success status
    """

    user_email = user.email
    first_name = user.first_name
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_token.make_token(user)

    verification_url = f'{domain}/verify-email/?uid={uid}&token={token}'

    data = {
        'verification_url': verification_url,
        'firstname': first_name
    }

    from_email = Email('welcome@etsea.com')
    to_email = To(user_email)
    subject = 'Email Verification'
    html_content = get_template('email-verification.html').render(data)
    content = Content('text/html', html_content)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)

    return True


def password_reset(user, domain):
    """
    Sends a password reset email to a user

    Args:
        user (webapp.models.User): The receiver User object
        domain (str): The site's domain

    Returns:
        bool: a boolean value representing success status
    """ 

    user_email = user.email
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_token.make_token(user)

    verification_url = f'{domain}/reset-password/?uid={uid}&token={token}'

    data = {
        'verification_url': verification_url
    }

    from_email = Email('help@etsea.com')
    to_email = To(user_email)
    subject = 'Reset Password'
    html_content = get_template('reset-password.html').render(data)
    content = Content("text/html", html_content)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)

    return True


def changed_password(user_email):
    """
    Sends a notification email to a user when password is changed

    Args:
        user_email (str): The receivers email
        first_name (str): The receivers first name

    Returns:
        bool: a boolean value representing success status
    """

    data = {

    }

    from_email = Email('help@realmax.com')
    to_email = To(user_email)
    subject = 'Password Changed'
    html_content = get_template('password-changed.html').render(data)
    content = Content("text/html", html_content)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)

    return True


def new_referral_registered(user_email, referral_name, first_name):
    """
    Sends a notification email to a user when a referral is registered with
    their code

    Args:
        user_email (str): The receivers email
        referral_name (str): The referrals name
        first_name (str): The receivers first name

    Returns:
        bool: a boolean value representing success status
    """

    data = {
        'first_name': first_name,
        'referral_name': referral_name
    }

    from_email = Email('help@realmax.com')
    to_email = To(user_email)
    subject = f'{referral_name} just registered with your code.'
    html_content = get_template('new-referral-registered.html').render(data)
    text_content = strip_tags(html_content)
    content = Content("text/html", text_content)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)

    return True


def commission_paid(user_email, amount):
    """
    Sends a notification email to a user on commission payment

    Args:
        user_email (str): The receivers email
        amount (float): Commission amount paid

    Returns:
        bool: a boolean value representing success status
    """

    data = {
        'amount': amount
    }

    from_email = Email('help@realmax.com')
    to_email = To(user_email)
    subject = f'NGN {amount} has been paid into your wallet.'
    html_content = get_template('commission_paid.html').render(data)
    text_content = strip_tags(html_content)
    content = Content("text/html", text_content)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)

    return True


def wallet_top_up(user_email, first_name, amount):
    """
    Sends a notification email to a user on wallet top-up

    Args:
        user_email (str): The receivers email
        first_name (str): The receivers first name
        amount (str): The amount paid into the wallet

    Returns:
        bool: a boolean value representing success status
    """

    data = {
        'amount': amount,
        'first_name': first_name
    }

    from_email = Email('help@realmax.com')
    to_email = To(user_email)
    subject = f'You topped up your REALMAX wallet with {amount}.'
    html_content = get_template('topup.html').render(data)
    text_content = strip_tags(html_content)
    content = Content("text/html", text_content)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)

    return True
