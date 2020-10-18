from celery import shared_task
import time
from django.core.mail import send_mail

@shared_task
def send_email_task():
    send_mail('Task Worked',
    'This is pr the task worked',
    'testuser.99@mail.ru',
    ['bakhytov.yerniyaz@gmail.com'])
    time.sleep(5)
    print("send email")
    # return None

