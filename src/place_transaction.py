import src.services.transactions as transactions
from src.utils.check_for_expired_card_date import is_expired
from src.utils.validate_card_format import validate_card_format
import json
import uuid
import datetime


def handler(event, context):
    body = json.loads(event["body"])
    if "card_id" not in body:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message": "Falure, No Credit Card detected. Please try again",
                    "result": "Declined",
                }
            ),
        }

    # checks to see if exp_date exists within payload
    if "exp_date" not in body:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message": "Falure, No expiration date detected. Please try again",
                    "result": "Declined",
                }
            ),
        }

    if not validate_card_format(body["card_id"]):
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message": "Falure, invlid Credit Card detected. Please try again",
                    "result": "Declined",
                }
            ),
        }

    # Calls the is_expired function to check exp_date from payload to see if expired or not,
    # True = Exp False = Not Exp
    is_expired_result = is_expired(body["exp_date"])
    print(f"Is expired: {is_expired_result}")

    # if true return response that says failure
    if is_expired_result:
        response_message = {
            "message": "Transaction Failed, the card you used is expired",
            "result": "Rejected",
        }

    # if false return "Happy Path" with time, result, message
    else:
        # Get the current timestamp
        current_timestamp = datetime.datetime.now().isoformat()
        response_message = {
            "message": "Transaction successful",
            "result": "Accepted",
            "timestamp": current_timestamp,  # Add the timestamp
        }

    transaction_id = str(uuid.uuid4())

    transaction_entry = {
        "PK": f"CARD_ID:{body['card_id']}",
        "SK": transaction_id,
        **body,
        "transaction_id": transaction_id,
    }

    transactions.put_transaction(transaction_entry)

    return {
        "statusCode": 200,
        "body": json.dumps(response_message),
    }
