import gspread
import logging
import requests

from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

from config import settings


logger = logging.getLogger(__name__)

SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

CONFIRMED = "Confirmed"
REJECTED = "Rejected"


def fix_number_formatting(number):
    if number:
        number = str(number)
        number = number.strip().replace(" ", "")
        if not number.startswith('+'):
            if not number.startswith('0'):
                return "0" + number
        else:
            if number.find("0") == 3:
                return number[:3] + number[4:]

    return number


def validate_phone_number(number):
    if number.startswith('0'):
        if len(number) != 11:
            return False
    if number.startswith('+'):
        if len(number) != 13:
            return False

    return True


def send_text_notification(data, status):
    if data['Mobil'] and data['Prenume']:

        if status == CONFIRMED:
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


def main():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(settings.SECRETS_FILE, SCOPE)
    gc = gspread.authorize(credentials)

    wks = gc.open_by_key(settings.DOCUMENT_KEY).sheet1

    row = 2
    for record in wks.get_all_records():
        if not record['Processed Timestamp']:
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
