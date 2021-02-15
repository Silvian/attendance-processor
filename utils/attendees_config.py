import requests

from config import settings


def get_attendees_config():
    headers = {
        "Accept": "application/json",
        "x-api-key": f"{settings.SETTINGS_API_KEY}",
    }
    response = requests.get(url=settings.SETTINGS_API_URL, headers=headers)
    if response.status_code != 200:
        return settings.ATTENDEES_MAX

    data = response.json()["body"]
    max_attendees = int(data["max"])
    return max_attendees
