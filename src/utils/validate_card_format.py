import re


def validate_card_format(card_number):
    pattern = re.compile(r"^\d{4}-\d{4}-\d{4}-\d{4}$")

    return bool(pattern.match(card_number))
