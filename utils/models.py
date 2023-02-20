import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


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
