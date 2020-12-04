import logging
import requests

from config import settings
from utils.phone_numbers import fix_number_formatting, validate_phone_number
from utils.states import AcceptanceStatus


logger = logging.getLogger(__name__)


def send_text_notification(data, status):
    if data['Mobil'] and data['Prenume']:

        if status == AcceptanceStatus.CONFIRMED:
            message = (
                f"Salutare {data['Prenume']}! Vă mulțumim pentru înscrierea la biserica din Harlesden pentru acest Sabat. "
                f"Prin acest text vă confirmăm că înscrierea dumneavoastră este confirmată. "
                f"Totuși, dacă din diferite motive nu veți putea ajunge, vă rugăm să ne informați prin secretara "
                f"bisericii noastre Iana la numarul de tel 07404 784 429. Vă mulțumim!"
            )
        else:
            message = (
                f"Salutare {data['Prenume']}! Din păcate înscrierea dumneavoastră la biserica din Harlesden pentru "
                f"Sabatul aceasta a eșuat, întrucât nu mai sunt locuri libere. "
                f"Vă mulțumim!"
            )

        number = fix_number_formatting(data['Mobil'])
        if not validate_phone_number(number):
            return False

        if settings.DEBUG == "true":
            logger.warning("Sending message to %s with body: %s", number, message)
            return True

        try:
            response = requests.post(
                url=settings.SMS_API_URL,
                headers={
                    'Content-Type': 'application/json',
                    'x-api-key': settings.SMS_API_KEY,
                },
                json={
                    "phone": number,
                    "country_code": settings.COUNTRY_CODE,
                    "sender_id": settings.SMS_SENDER_ID,
                    "message": message,
                }
            )
            if response.status_code == 200:
                return True

        except requests.exceptions.ConnectionError:
            pass

    return False
