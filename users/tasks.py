from goodreads.celery import app
from django.core.mail import send_mail


@app.task()
def send_email(subject, message, recipient_list):
    send_mail(
        subject, message, 'djangomail669@gmail.com', recipient_list
    )
