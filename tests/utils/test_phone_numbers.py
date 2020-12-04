import pytest


from utils.phone_numbers import fix_number_formatting, validate_phone_number


@pytest.mark.parametrize(
    "number, expected_result",
    [
        ("7446123456", "07446123456"),  # Test number with missing 0
        ("07446123456", "07446123456"),  # Test number no spaces
        ("07446 123456", "07446123456"),  # Test number with spaces
        ("+447446123456", "+447446123456"),  # Test international number no spaces
        ("+447446 123456", "+447446123456"),  # Test international number with spaces
        ("+4407446123456", "+447446123456"),  # Test international number with a 0
        ("+44 07446 123456", "+447446123456"),  # Test international number with a 0 and spaces
    ],
)
def test_fix_number_formatting(number, expected_result):
    result = fix_number_formatting(number)
    assert expected_result == result


@pytest.mark.parametrize(
    "number, expected_result",
    [
        ("07446123456", True),  # Test number is valid
        ("074461234567", False),  # Test number is too long
        ("+447446123456", True),  # Test international number is valid
        ("+4407446123456", False),  # Test international number contains 0
        ("+4474461234567", False),  # Test international number is too long 0
    ]
)
def test_validate_phone_number(number, expected_result):
    result = validate_phone_number(number)
    assert expected_result == result
