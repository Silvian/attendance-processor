import logging
import requests

from config import settings


logger = logging.getLogger(__name__)


def send_text_notification(data, number, message):
    message = f"Salutare {data['Prenume']}! " + message

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
