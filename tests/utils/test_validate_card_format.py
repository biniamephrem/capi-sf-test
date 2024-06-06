from src.utils.validate_card_format import validate_card_format


def test_validate_card_format_happy():
    result = validate_card_format("1234-1234-1234-1234")

    assert result is True


def test_validate_card_format_wrong_1():
    result = validate_card_format("1234-1234-1234-123")

    assert result is False


def test_validate_card_format_wrong_2():
    result = validate_card_format("ABCD-1234-1234-1234")

    assert result is False
