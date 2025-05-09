from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_token_email(email, token):
    subject = "Your API Token"
    message = f"Welcome! Your authentication token is: {token}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
