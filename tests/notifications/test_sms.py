import pytest
import mock

from notifications.sms import send_text_notification


@mock.patch("requests.post")
@pytest.mark.parametrize(
    "data, status, expected_result",
    [
        (
            {"Mobil": "07446123456", "Prenume": "Test"},
            "Confirmed",
            True,
        ),
    ]
)
def test_send_text_notification(mocker, data, status, expected_result):
    mocker.return_value.status_code = 200
    result = send_text_notification(data, status)
    assert expected_result == result


@mock.patch("requests.post")
@pytest.mark.parametrize(
    "data, status, expected_result",
    [
        (
            {"Mobil": "074461234560", "Prenume": "Test"},
            "Confirmed",
            False,
        ),
    ]
)
def test_send_text_notification_invalid_number(mocker, data, status, expected_result):
    mocker.return_value.status_code = 200
    result = send_text_notification(data, status)
    assert expected_result == result


@mock.patch("requests.post")
@pytest.mark.parametrize(
    "data, status, expected_result",
    [
        (
            {"Mobil": "7446123456", "Prenume": "Test"},
            "Confirmed",
            True,
        ),
    ]
)
def test_send_text_notification_missing_zero_number(mocker, data, status, expected_result):
    mocker.return_value.status_code = 200
    result = send_text_notification(data, status)
    assert expected_result == result
