import re


def validate_email_address(email):
    if email:
        if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            return True

    return False
