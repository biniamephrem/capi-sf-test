import json


def prepare_API_payload(body):
    return {
        "body": json.dumps(body),
    }


def extract_API_pyload_body(payload):
    return json.loads(payload["body"])
