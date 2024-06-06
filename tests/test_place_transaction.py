from src.place_transaction import handler
from helpers import prepare_API_payload, extract_API_pyload_body

import src.services.transactions  # noqa: F401, E261


def test_handler_missing_cc_id():
    result = handler(prepare_API_payload({"exp_date": "05/25"}), None)

    assert result["statusCode"] == 400

    body = extract_API_pyload_body(result)
    assert body["message"] == "Falure, No Credit Card detected. Please try again"
    assert body["result"] == "Declined"


def test_handler_missing_cc_id_and_exp_date():
    result = handler(prepare_API_payload({}), None)
    assert result["statusCode"] == 400

    body = extract_API_pyload_body(result)
    assert body["message"] == "Falure, No Credit Card detected. Please try again"
    assert body["result"] == "Declined"


def test_handler_invalid_cc():
    result = handler(prepare_API_payload({"card_id": "Mickey Mouse", "exp_date": "05/25"}), None)
    assert result["statusCode"] == 400

    body = extract_API_pyload_body(result)
    assert body["message"] == "Falure, invlid Credit Card detected. Please try again"
    assert body["result"] == "Declined"


def test_handler_missing_exp_date():
    result = handler(prepare_API_payload({"card_id": "1234"}), None)

    assert result["statusCode"] == 400

    body = extract_API_pyload_body(result)
    assert body["message"] == "Falure, No expiration date detected. Please try again"
    assert body["result"] == "Declined"


def test_handler_date_expired(mocker):
    put_transaction_mock = mocker.patch("src.services.transactions.put_transaction", return_value=True)

    result = handler(
        prepare_API_payload(
            {"card_id": "1111-2222-3333-4444", "exp_date": "06/23"},
        ),
        None,
    )

    put_transaction_mock.assert_called_once()
    assert result["statusCode"] == 200

    body = extract_API_pyload_body(result)
    assert body["message"] == "Transaction Failed, the card you used is expired"
    assert body["result"] == "Rejected"


def test_handler_happy(mocker):
    put_transaction_mock = mocker.patch("src.services.transactions.put_transaction", return_value=True)

    result = handler(
        prepare_API_payload(
            {"card_id": "1111-2222-3333-4444", "exp_date": "06/25"},
        ),
        None,
    )

    put_transaction_mock.assert_called_once()
    assert result["statusCode"] == 200

    body = extract_API_pyload_body(result)
    assert body["message"] == "Transaction successful"
    assert body["result"] == "Accepted"
