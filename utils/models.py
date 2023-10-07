import json
import logging

import boto3
from django.conf import settings
from django.db import models

logger = logging.getLogger(__name__)


class DownloadableFile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to="downloadable_files/")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class GPTModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    primary = models.BooleanField(default=False)

    def __str__(self):
        return self.name


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
    parameters = models.TextField(blank=True, null=True)

    recipient = models.EmailField()

    sent = models.BooleanField(default=False)

    # These will be generated on send
    text_body = models.TextField(blank=True, null=True)
    html_body = models.TextField(blank=True, null=True)

    def set_parameters(self, parameters):
        self.parameters = json.dumps(parameters)
        self.save()

    def get_parameters(self):
        return json.loads(self.parameters)
