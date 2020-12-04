import gspread
import logging

from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

from config import settings
from notifications.sms import send_text_notification
from utils.states import AcceptanceStatus


logger = logging.getLogger(__name__)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(settings.SECRETS_FILE, scope)
gc = gspread.authorize(credentials)

wks = gc.open_by_key(settings.DOCUMENT_KEY).sheet1


def main():
    # Process worksheet
    row = 2
    for record in wks.get_all_records():
        if not record['Processed Timestamp']:
            if row <= settings.ATTENDEES_MAX + 1:
                status = AcceptanceStatus.CONFIRMED
            else:
                status = AcceptanceStatus.REJECTED

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
