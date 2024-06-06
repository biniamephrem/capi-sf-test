import boto3
from boto3.dynamodb.conditions import Key
import decimal
import json
import os

AWS_REGION = os.environ.get("AWS_REGION", "us-west-2")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)


class DecimalEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)

        return super(DecimalEncoder, self).default(o)


def put_item(table_name, item):
    table = dynamodb.Table(table_name)
    response = table.put_item(Item=item)

    return response


def query(table_name, pk, sk=None, ascending=True, ProjectionExpression=[], with_ttl=False):
    search_criteria = Key("PK").eq(pk) if sk is None else Key("PK").eq(pk) & Key("SK").eq(sk)
    table = dynamodb.Table(table_name)

    if len(ProjectionExpression) > 0:
        response = table.query(
            KeyConditionExpression=search_criteria,
            ScanIndexForward=ascending,
            ProjectionExpression=",".join(ProjectionExpression),
            Select="SPECIFIC_ATTRIBUTES",
        )
    else:
        response = table.query(KeyConditionExpression=search_criteria, ScanIndexForward=ascending)

    results = [
        {key: val for key, val in Item.items() if key != "ttl" or with_ttl}
        for Item in (response["Items"] if "Items" in response else [])
    ]

    return json.loads(json.dumps(results, cls=DecimalEncoder))
