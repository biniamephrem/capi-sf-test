import src.rules.transaction as Transaction


def handler(event, context):
    payload = event["payload"]
    rules = event["rules"]
    result = False

    for rule in rules:
        result = result and getattr(Transaction, rule)(payload)

    return result
