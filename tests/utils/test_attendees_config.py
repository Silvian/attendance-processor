import pytest
import mock

from utils.attendees_config import get_attendees_config


@mock.patch("requests.get")
@mock.patch("config.settings.ATTENDEES_MAX", 100)
def test_get_attendees_config(mocker):
    max_attendees = 50
    mocker.return_value.status_code = 200
    mocker.return_value.json.return_value = {
        "body": {
            "key": "attendees",
            "max": max_attendees,
        }
    }
    result = get_attendees_config()
    assert max_attendees == result


@mock.patch("requests.get")
@mock.patch("config.settings.ATTENDEES_MAX", 100)
def test_get_attendees_config_failed_api(mocker):
    max_attendees = 100
    mocker.return_value.status_code = 500
    result = get_attendees_config()
    assert max_attendees == result
