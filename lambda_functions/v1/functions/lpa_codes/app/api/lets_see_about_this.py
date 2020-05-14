import boto3

from . import code_generator
from .helpers import custom_logger
import os

logger = custom_logger()


def db_connection():
    if os.environ.get("ENVIRONMENT") in ["ci", "local"]:
        conn = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
    else:
        conn = boto3.resource("dynamodb")

    return conn


def handle_create(data):
    """
    Placeholder for create a code endpoint
    Returns:
    json
    """

    db = db_connection()

    code_list = []

    for entry in data["lpas"]:

        key = {"lpa": entry["lpa"], "actor": entry["actor"]}

        # 1. expire all existing codes for LPA/Actor combo
        code_generator.update_codes(database=db, key=key, status=False)

        # 2. generate a new code
        generated_code = code_generator.generate_code(database=db)

        # 3. insert new code into database
        new_code = code_generator.insert_new_code(
            database=db, key=key, code=generated_code
        )[0]["code"]

        # 4. return the new code in lambda payload
        response = {
            "lpa": entry["lpa"],
            "actor": entry["actor"],
            "code": new_code,
        }

        code_list.append(response)

    return code_list
