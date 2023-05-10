import logging

import boto3
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class AdminPhoneNumber(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    number = models.CharField(max_length=255)

    def __str__(self):
        return self.number


class AdminEmail(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    email = models.EmailField()

    def __str__(self):
        return self.email


class TextMessage(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    recipient = models.CharField(max_length=255)

    message = models.TextField()

    sent = models.BooleanField(default=False)

    def send(self):
        if self.sent:
            logger.warning("Message already sent")
            return False

        sns = boto3.client(
            "sns",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name="us-east-1",
        )
        sns.publish(PhoneNumber=self.recipient, Message=self.message)

        self.sent = True
        self.save()


class Email(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    template = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)

    recipient = models.EmailField()

    sent = models.BooleanField(default=False)

    # These will be generated on send
    text_body = models.TextField(blank=True, null=True)
    html_body = models.TextField(blank=True, null=True)

    def send(self, parameters):
        if self.sent:
            logger.warning("Email already sent")
            return False

        text_body = render_to_string("email/{}.txt".format(self.template), parameters)
        html_body = render_to_string("email/{}.html".format(self.template), parameters)

        emails = [self.recipient]

        send_mail(
            self.subject,
            text_body,
            settings.DEFAULT_FROM_EMAIL,
            emails,
            html_message=html_body,
            fail_silently=True,
        )

        self.text_body = text_body
        self.html_body = html_body
        self.sent = True
        self.save()
