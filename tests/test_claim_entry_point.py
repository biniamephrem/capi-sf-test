from src.claim_entry_point import handler
from helpers import prepare_API_payload, extract_API_pyload_body


import uuid  # noqa: F401, E261
import src.services.aws.dynamodb  # noqa: F401, E261
import src.services.aws.step_function  # noqa: F401, E261


def test_handler_missing_cc_id_and_exp_date():
    result = handler(prepare_API_payload({}), None)
    assert result["statusCode"] == 400

    body = extract_API_pyload_body(result)
    assert body["message"] == "Falure, No Credit Card detected. Please try again"
    assert body["result"] == "Declined"


def test_handler_missing_cc_id():
    result = handler(prepare_API_payload({"transaction_id": "Mickey Mosuse"}), None)

    assert result["statusCode"] == 400

    body = extract_API_pyload_body(result)
    assert body["message"] == "Falure, No Credit Card detected. Please try again"
    assert body["result"] == "Declined"
# For testing code 

def test_handler_missing_transaction_id():
    result = handler(prepare_API_payload({"card_id": "Mickey Mosuse"}), None)

    assert result["statusCode"] == 400

    body = extract_API_pyload_body(result)
    assert body["message"] == "Falure, No transaction_id detected. Please try again"
    assert body["result"] == "Declined"


def test_handler_invalid_cc():
    result = handler(prepare_API_payload({"card_id": "Mickey Mouse", "transaction_id": "123"}), None)
    assert result["statusCode"] == 400

    body = extract_API_pyload_body(result)
    assert body["message"] == "Falure, invlid Credit Card detected. Please try again"
    assert body["result"] == "Declined"


# TODO test the format of transaction_id


def test_handler_happy(mocker):
    put_item_mock = mocker.patch("src.services.aws.dynamodb.put_item", return_value=True)
    start_execution_mock = mocker.patch("src.services.aws.step_function.start_execution", return_value=True)
    uuid_mock = mocker.patch("uuid.uuid4", return_value="Micky Mosuse")

    result = handler(
        prepare_API_payload(
            {"card_id": "1111-2222-3333-4444", "transaction_id": "123"},
        ),
        None,
    )

    put_item_mock.assert_called_once()
    start_execution_mock.assert_called_once()
    uuid_mock.assert_called_once()

    assert result["statusCode"] == 200
    body = extract_API_pyload_body(result)
    assert body["transaction_id"] == "123"
    assert body["claim_id"] == "Micky Mosuse"
