import gspread

from oauth2client.service_account import ServiceAccountCredentials

from config import settings

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(settings.SECRETS_FILE, scope)
gc = gspread.authorize(credentials)

wks = gc.open_by_key(settings.DOCUMENT_KEY).sheet1
wks.range = {"startRowIndex": 1}


def main():
    # Clear worksheet
    total_rows = len(wks.get_all_values())
    start_index = 2
    end_index = start_index + total_rows
    wks.delete_rows(start_index=start_index, end_index=end_index)
    wks.add_rows(rows=total_rows)


if __name__ == "__main__":
    # Run cleaner
    main()
