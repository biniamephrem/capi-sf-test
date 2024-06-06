from src.valid_transaction_rule_one import handler


def test_handler():
    result = handler({}, None)

    assert result is True
