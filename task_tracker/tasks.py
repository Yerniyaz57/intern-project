from __future__ import absolute_import
from celery import shared_task
from django.core.mail import send_mail
# from project.celery import app


@shared_task
def send_email_task(email, text):
    send_mail('Message',
    text,
    'testuser.99@mail.ru',
    [email])
    print("send email")
    return None
