from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


@shared_task
def send_activation_email(username, email):
    subject = 'Sign Up'
    message_body = f'''
            Activation Link:
            {settings.HTTP_SCHEMA}://{settings.DOMAIN}{reverse('accounts:activate-user', args=[username])}
            '''
    email_from = settings.EMAIL_HOST_USER
    send_mail(
        subject,
        message_body,
        email_from,
        [email],
        fail_silently=False
    )
