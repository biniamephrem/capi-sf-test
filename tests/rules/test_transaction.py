from src.rules.transaction import rule_1


def test_transaction_rule_1():
    result = rule_1({})

    assert result is True
