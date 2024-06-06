import boto3
import json
import os

AWS_REGION = os.environ.get("AWS_REGION", "us-west-2")

step_function_client = boto3.client("stepfunctions", region_name=AWS_REGION)


def start_execution(state_machine_arn, name, payload):
    reponse = step_function_client.start_execution(
        stateMachineArn=state_machine_arn,
        # name=name[:79],
        input=json.dumps(payload),
    )

    return reponse
