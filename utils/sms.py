from utils.models import AdminPhoneNumber, TextMessage


def create_admin_sms(message):
    admin_phone_numbers = AdminPhoneNumber.objects.all()
    for admin_phone_number in admin_phone_numbers:
        text_message = TextMessage.objects.create(
            recipient=admin_phone_number.number,
            message=message,
        )
        text_message.send()
