from src.services.transactions import get_transaction


def handler(event, context):
    print(event)

    # using same table for transaction as well as for claims - lazy way
    transaction = get_transaction(event["transaction_id"])

    return transaction
