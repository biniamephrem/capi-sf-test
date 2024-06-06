import src.services.aws.step_function as step_function
import src.services.aws.dynamodb as dynamodb
from src.utils.validate_card_format import validate_card_format

import uuid
import json
import os

ORCHESTRATION_STATE_MACHINE_ARN = os.environ.get("ORCHESTRATION_STATE_MACHINE_ARN", "")
CLAIMS_TABLE_NAME = os.environ.get("CLAIMS_TABLE_NAME", "")


def handler(event, context):
    print(event)
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

    if "transaction_id" not in body:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {
                    "message": "Falure, No transaction_id detected. Please try again",
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

    # TODO crate if statment for checking transaction_id format

    # TODO create clain record in DynamoDB table
    claim_id = str(uuid.uuid4())

    claim_entry = {
        "PK": f"CLAIM:{claim_id}",
        "SK": "CLAIM-START",
        "transaction_id": body["transaction_id"],
    }

    dynamodb.put_item(CLAIMS_TABLE_NAME, claim_entry)

    # prepare payload
    payload = {
        "claim_id": claim_id,
        "transaction_id": body["transaction_id"],
    }

    # start claim orchestration flow
    step_function.start_execution(ORCHESTRATION_STATE_MACHINE_ARN, None, payload)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "transaction_id": body["transaction_id"],
                "claim_id": claim_id,
            }
        ),
    }
