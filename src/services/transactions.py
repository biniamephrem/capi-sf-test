from src.services.aws.dynamodb import query, put_item
import os


TRANSACTIONS_TABLE_NAME = os.environ.get("TRANSACTIONS_TABLE_NAME", "")


def get_transaction(transaction_id):
    transactions = query(TRANSACTIONS_TABLE_NAME, f"TRANSACTION:{transaction_id}")

    if len(transactions) == 0:
        return None

    return transactions[0]


def put_transaction(payload):
    response = put_item(TRANSACTIONS_TABLE_NAME, payload)

    return response
