import pytest


from utils.emails import validate_email_address


@pytest.mark.parametrize(
    "email, expected_result",
    [
        ("test@example.com", True),  # Test valid email address.
        ("test.example.com", False),  # Test invalid email address.
        ("garbage", False),  # Test garbage entry.
        ("@.com", False),  # Test only email key characters.
        ("", False),  # Test empty email field.
    ]
)
def test_validate_email_address(email, expected_result):
    result = validate_email_address(email)
    assert expected_result == result
