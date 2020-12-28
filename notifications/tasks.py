import logging

from config import settings
from notifications.email import send_email_notification
from notifications.sms import send_text_notification
from utils.emails import validate_email_address
from utils.phone_numbers import fix_number_formatting, validate_phone_number
from utils.states import AcceptanceStatus


logger = logging.getLogger(__name__)


def send_notification(data, status):
    if data['Email'] and data['Mobil'] and data['Prenume']:

        if status == AcceptanceStatus.CONFIRMED:
            subject = "Înscrierea ta a fost înregistrată cu sucess"
            message = (
                f"Vă mulțumim pentru înscrierea la biserica din Harlesden pentru acest Sabat. "
                f"Prin acest mesaj vă confirmăm că înscrierea dumneavoastră este confirmată. "
                f"Totuși, dacă din diferite motive nu veți putea ajunge, vă rugăm să ne informați prin secretara "
                f"bisericii noastre Iana la numarul de tel 07404 784 429. Vă mulțumim!"
            )
        else:
            subject = "Înscrierea ta a eșuat"
            message = (
                f"Din păcate înscrierea dumneavoastră la biserica din Harlesden pentru "
                f"Sabatul aceasta a eșuat, întrucât nu mai sunt locuri libere. "
                f"Vă mulțumim!"
            )

        if settings.SMS_ALERTS == "true":
            number = fix_number_formatting(data['Mobil'])
            if not validate_phone_number(number):
                return False

            if settings.DEBUG == "true":
                logger.warning("Sending message to %s with body: %s", number, message)
                return True

            return send_text_notification(data, number, message)

        if not validate_email_address(data['Email']):
            return False

        if settings.DEBUG == "true":
            logger.warning(
                "Sending email to %s with subject %s and body: %s",
                data['Email'], subject, message
            )
            return True

        return send_email_notification(data, subject, message)
