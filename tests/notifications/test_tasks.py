import pytest
import mock

from notifications.tasks import send_notification


@mock.patch("requests.post")
@mock.patch("config.settings.SMS_ALERTS", "true")
@pytest.mark.parametrize(
    "data, status, expected_result",
    [
        (
            {"Email": "test@example.com", "Mobil": "07446123456", "Prenume": "Test"},
            "Confirmed",
            True,
        ),
    ]
)
def test_send_sms_notification(mocker, data, status, expected_result):
    mocker.return_value.status_code = 200
    result = send_notification(data, status)
    assert expected_result == result


@mock.patch("requests.post")
@mock.patch("config.settings.SMS_ALERTS", "true")
@pytest.mark.parametrize(
    "data, status, expected_result",
    [
        (
            {"Email": "test@example.com", "Mobil": "074461234560", "Prenume": "Test"},
            "Confirmed",
            False,
        ),
    ]
)
def test_send_sms_notification_invalid_number(mocker, data, status, expected_result):
    mocker.return_value.status_code = 200
    result = send_notification(data, status)
    assert expected_result == result


@mock.patch("requests.post")
@mock.patch("config.settings.SMS_ALERTS", "true")
@pytest.mark.parametrize(
    "data, status, expected_result",
    [
        (
            {"Email": "test@example.com", "Mobil": "7446123456", "Prenume": "Test"},
            "Confirmed",
            True,
        ),
    ]
)
def test_send_sms_notification_missing_zero_number(mocker, data, status, expected_result):
    mocker.return_value.status_code = 200
    result = send_notification(data, status)
    assert expected_result == result


@mock.patch("config.settings.SMS_ALERTS", "false")
@pytest.mark.parametrize(
    "data, status, expected_result",
    [
        (
            {"Email": "test@example.com", "Mobil": "07446123456", "Prenume": "Test"},
            "Confirmed",
            True,
        ),
    ]
)
def test_send_email_notification(data, status, expected_result):
    result = send_notification(data, status)
    assert expected_result == result


@mock.patch("config.settings.SMS_ALERTS", "false")
@pytest.mark.parametrize(
    "data, status, expected_result",
    [
        (
            {"Email": "test.example.com", "Mobil": "07446123456", "Prenume": "Test"},
            "Confirmed",
            False,
        ),
    ]
)
def test_send_email_notification_invalid_email(data, status, expected_result):
    result = send_notification(data, status)
    assert expected_result == result
