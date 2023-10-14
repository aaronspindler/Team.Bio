import csv
from io import StringIO

from celery import shared_task
from django.urls import reverse

from accounts.models import User
from companies.models import BulkInviteRequest, Invite
from utils.models import Email
from utils.tasks import send_email


@shared_task
def process_bulk_invite_request(bulk_invite_request_pk):
    bulk_invite_request = BulkInviteRequest.objects.get(pk=bulk_invite_request_pk)
    if bulk_invite_request.processed:
        return False

    company = bulk_invite_request.company
    requester = bulk_invite_request.requested_by

    file = bulk_invite_request.file.read().decode("utf-8")
    reader = csv.DictReader(StringIO(file), delimiter=",")
    for row in reader:
        email = row["Email"]
        # Check if the user exists already, or a pending invite already exists
        # If so, skip this row
        if User.objects.filter(email__icontains=email).exists():
            continue
        if Invite.objects.filter(email__icontains=email).exists():
            continue
        if row["Deactivated date (UTC)"] != "":
            continue

        # Create a new invite
        # Invite.objects.create(company=company, email=email) # Commented out for testing

        # Email the invited user
        parameters = {
            "invite_sender_name": requester.name,
            "invite_sender_organization_name": company.name,
            "action_url": f"https://www.team.bio{reverse('account_login')}",
            "recipient_name": row["Name"],
        }

        # Send an invitation email
        email_to_send = Email.objects.create(
            recipient="aaron@team.bio",  # Change this email after testing
            template="invite",
            subject=f"You have been invited by {requester.name} to join your {company.name} co-workers on Team Bio",
        )
        email_to_send.set_parameters(parameters)
        send_email.delay(email_to_send.pk)

    # Send a success email to the requester
    success_email_to_send = Email.objects.create(
        recipient=requester.email,
        template="bulk_invite_success",
        subject=f"Team Bio Bulk Invite Processed Successfully For {company.name}",
    )
    send_email.delay(success_email_to_send.pk)

    bulk_invite_request.processed = True
    bulk_invite_request.save()
