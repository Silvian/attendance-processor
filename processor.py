import gspread
import logging
import requests

from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from config import settings


logger = logging.getLogger(__name__)


CONFIRMED = "Confirmed"
REJECTED = "Rejected"

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(settings.SECRETS_FILE, scope)
gc = gspread.authorize(credentials)

wks = gc.open_by_key(settings.DOCUMENT_KEY).sheet1


def fix_number_formatting(number):
    if number:
        number = str(number)
        if not number.startswith('+'):
            if not number.startswith('0'):
                return "0" + number

    return number


def send_text_notification(data, status):
    if data['Mobile'] and data['First Name']:

        if status == CONFIRMED:
            message = (
                f"Hi {data['First Name']}! Thank you for registering to visit Harlesden church this coming sabbath. "
                f"Your attendance has been confirmed and we hope to see you there!"
            )
        else:
            message = (
                f"Hi {data['First Name']}! Thank you for registering to visit Harlesden church this coming sabbath. "
                f"Unfortunately due to high demand the max number of people attending has been reached. "
                f"You cannot attend this sabbath."
            )

        if settings.DEBUG == "true":
            logger.warning("Sending message to %s with body: %s", data['Mobile'], message)
            return True

        try:
            response = requests.post(
                url=settings.SMS_API_URL,
                headers={
                    'Content-Type': 'application/json',
                    'x-api-key': settings.SMS_API_KEY,
                },
                json={
                    "phone": fix_number_formatting(data['Mobile']),
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


def main():
    row = 2
    for record in wks.get_all_records():
        if not record['Processed timestamp']:
            if row <= settings.ATTENDEES_MAX + 1:
                status = CONFIRMED
            else:
                status = REJECTED

            if send_text_notification(record, status):
                cell = "F" + str(row)
                wks.update_acell(cell, status)
                cell = "G" + str(row)
                wks.update_acell(cell, str(datetime.now()))

        row += 1


if __name__ == "__main__":
    # Run processor
    if settings.DEBUG == "true":
        logger.warning("Running in DEBUG mode")
    main()
