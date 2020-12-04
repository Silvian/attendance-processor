
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
