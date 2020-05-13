import datetime
import secrets
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
from .helpers import custom_logger

logger = custom_logger("code generator")


def generate_code():
    """
    Generates a 12-digit alphanumeric code containing no ambiguous characters.
    Codes should be unique.
    Codes should not be reused.

    Returns:
        string
    """
    acceptable_characters = "23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"

    unique = False
    attempts = 0
    max_attempts = 10

    while unique is not True:
        new_code = "".join(secrets.choice(acceptable_characters) for i in range(0, 12))
        # unique = check_code_unique(new_code)
        unique = True
        attempts += 1
        if attempts == max_attempts:
            logger.error("Unable to generate unique code - failed after 10 attempts")
            new_code = None
            break
    return new_code


def check_code_unique(code):
    """
    Check the new code we've generated has not been used before
    Args:
        code: string

    Returns:
        boolean
    """
    response = get_codes(code=code)

    print(f"response: {response}")

    if len(response) == 0:
        return True
    return False


def get_dynamodb():
    environment = os.environ["ENVIRONMENT"]
    if environment == "ci":
        return boto3.resource(
            "dynamodb", endpoint_url="http://localhost:8000", region_name="eu-west-1"
        )
    else:
        return boto3.resource("dynamodb")


def get_codes(key=None, code=None):
    table = get_dynamodb().Table("lpa_codes")
    return_fields = "lpa, actor, code, active, last_updated_date"

    codes = []

    if code:
        query_result = table.get_item(
            Key={"code": code}, ProjectionExpression=return_fields
        )

        try:
            codes.append(query_result["Item"])
        except KeyError:
            # TODO better error handling here
            logger.info("Code does not exist in database")

    elif key:
        lpa = key["lpa"]
        actor = key["actor"]
        query_result = table.query(
            IndexName="key_index",
            KeyConditionExpression=Key("lpa").eq(lpa),
            FilterExpression=Attr("actor").eq(actor),
            ProjectionExpression=return_fields,
        )

        if len(query_result["Items"]) > 0:
            codes.extend(query_result["Items"])
        else:
            # TODO better error handling here
            logger.info("LPA/actor does not exist in database")

    return codes


def update_codes(key=None, code=None, status=False):
    table = get_dynamodb().Table("lpa_codes")

    entries = get_codes(key=key, code=code)

    updated_rows = 0
    for entry in entries:
        if entry["active"] != status:

            table.update_item(
                Key={"code": entry["code"]},
                UpdateExpression="set active = :a, last_updated_date = :d",
                ExpressionAttributeValues={
                    ":a": status,
                    ":d": datetime.datetime.now().strftime("%d/%m/%Y"),
                },
            )

            updated_rows += 1
    logger.info(f"{updated_rows} rows updated for LPA/Actor")
    return updated_rows


def insert_new_code(key, code):
    table = get_dynamodb().Table("lpa_codes")
    lpa = key["lpa"]
    actor = key["actor"]

    table.put_item(
        Item={
            "lpa": lpa,
            "actor": actor,
            "code": code,
            "active": True,
            "last_updated_date": datetime.datetime.now().strftime("%d/%m/%Y"),
        }
    )

    inserted_item = get_codes(code=code)

    return inserted_item
