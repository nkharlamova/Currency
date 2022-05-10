from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_email(email_from, reply_to, subject, message):
    recipient = settings.EMAIL_HOST_USER
    body = f'''
            Request From: {email_from}
            Email to reply: {reply_to}
            Subject: {subject}
            Body: {message}
            '''
    send_mail(
        subject,
        body,
        recipient,
        [recipient],
        fail_silently=False,
    )
