from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from utils.models import AdminPhoneNumber, Email, TextMessage


@shared_task
def create_admin_sms(message):
    admin_phone_numbers = AdminPhoneNumber.objects.all()
    for admin_phone_number in admin_phone_numbers:
        text_message = TextMessage.objects.create(
            recipient=admin_phone_number.number,
            message=message,
        )
        text_message.send()


@shared_task
def send_email(email_pk):
    email = Email.objects.get(pk=email_pk)
    if email.sent:
        return False

    parameters = email.get_parameters()

    text_body = render_to_string("email/{}.txt".format(email.template), parameters)
    html_body = render_to_string("email/{}.html".format(email.template), parameters)

    emails = [email.recipient]

    send_mail(
        email.subject,
        text_body,
        settings.DEFAULT_FROM_EMAIL,
        emails,
        html_message=html_body,
        fail_silently=True,
    )

    email.text_body = text_body
    email.html_body = html_body
    email.sent = True
    email.save()
