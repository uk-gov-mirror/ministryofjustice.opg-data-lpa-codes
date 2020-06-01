from copy import deepcopy

from pytest_cases import CaseData, case_name

from lambda_functions.v1.tests.conftest import test_constants

default_test_data = [
    {
        "active": True,
        "actor": "mediumblue",
        "code": "YsSu4iAztUXm",
        "expiry_date": test_constants["EXPIRY_DATE"],
        "generated_date": "29/03/2020",
        "last_updated_date": "25/08/2020",
        "dob": "1960-06-05",
        "lpa": "drive_leading-edge_communities",
    },
    {
        "active": True,
        "actor": "mediumblue",
        "code": "aEYVS6i9zSwy",
        "expiry_date": test_constants["EXPIRY_DATE"],
        "generated_date": "27/06/2019",
        "last_updated_date": "03/02/2020",
        "dob": "1960-06-05",
        "lpa": "drive_leading-edge_communities",
    },
    {
        "active": True,
        "actor": "mediumblue",
        "code": "ZY577rXcRVLY",
        "expiry_date": test_constants["EXPIRY_DATE"],
        "generated_date": "05/04/2020",
        "last_updated_date": "28/02/2021",
        "dob": "1960-06-05",
        "lpa": "drive_leading-edge_communities",
    },
    {
        "active": False,
        "actor": "mediumblue",
        "code": "hFCarGyJF6G2",
        "expiry_date": test_constants["EXPIRY_DATE"],
        "generated_date": "07/08/2019",
        "last_updated_date": "24/03/2020",
        "dob": "1960-06-05",
        "lpa": "drive_leading-edge_communities",
    },
    {
        "active": False,
        "actor": "mediumblue",
        "code": "hm8Qtyb763tD",
        "expiry_date": test_constants["EXPIRY_DATE"],
        "generated_date": "06/08/2019",
        "last_updated_date": "01/12/2019",
        "dob": "1960-06-05",
        "lpa": "drive_leading-edge_communities",
    },
    {
        "active": False,
        "actor": "mediumblue",
        "code": "HiRqUNXRKB3X",
        "expiry_date": test_constants["EXPIRY_DATE"],
        "generated_date": "03/01/2020",
        "last_updated_date": "11/04/2020",
        "dob": "1960-06-05",
        "lpa": "drive_leading-edge_communities",
    },
    {
        "active": False,
        "actor": "mediumblue",
        "code": "UEW7zSi42bLF",
        "expiry_date": test_constants["EXPIRY_DATE"],
        "generated_date": "09/03/2020",
        "last_updated_date": "17/10/2020",
        "dob": "1960-06-05",
        "lpa": "drive_leading-edge_communities",
    },
]


@case_name("Get codes by key")
def case_get_codes_1() -> CaseData:
    test_data = deepcopy(default_test_data)
    code = None
    key = {
        "lpa": "drive_leading-edge_communities",
        "actor": "mediumblue",
    }

    expected_result = code
    expected_result_count = 7
    expected_logger_message = None
    return (
        test_data,
        code,
        key,
        expected_result,
        expected_result_count,
        expected_logger_message,
    )


@case_name("Get codes by key that doesn't exist")
def case_get_codes_11() -> CaseData:
    test_data = deepcopy(default_test_data)
    code = None
    key = {
        "lpa": "fake_lpa_id",
        "actor": "fake_actor",
    }

    expected_result = None
    expected_result_count = 0
    expected_logger_message = "LPA/actor does not exist in database"
    return (
        test_data,
        code,
        key,
        expected_result,
        expected_result_count,
        expected_logger_message,
    )


@case_name("Get codes by code")
def case_get_codes_2() -> CaseData:
    test_data = deepcopy(default_test_data)
    code = "ZY577rXcRVLY"
    key = None

    expected_result = code
    expected_result_count = 1
    expected_logger_message = None

    return (
        test_data,
        code,
        key,
        expected_result,
        expected_result_count,
        expected_logger_message,
    )


@case_name("Get codes by code that doesn't exist")
def case_get_codes_21() -> CaseData:
    test_data = deepcopy(default_test_data)
    code = "fake_code"
    key = None

    expected_result = None
    expected_result_count = 0
    expected_logger_message = "Code does not exist in database"
    return (
        test_data,
        code,
        key,
        expected_result,
        expected_result_count,
        expected_logger_message,
    )


@case_name("Get codes by both code and key")
def case_get_codes_3() -> CaseData:
    """
    If both key and code are supplied, code should be preferred as it is guaranteed
    to be unique
    """

    test_data = deepcopy(default_test_data)
    code = "ZY577rXcRVLY"
    key = {
        "lpa": "drive_leading-edge_communities",
        "actor": "mediumblue",
    }

    expected_result = code
    expected_result_count = 1
    expected_logger_message = None

    return (
        test_data,
        code,
        key,
        expected_result,
        expected_result_count,
        expected_logger_message,
    )


@case_name("Get codes by key that is past TTL")
def case_get_codes_13() -> CaseData:
    """
    TTL rows are not removed immediately, to be sure you are not returning any expired
    rows in a query you should exclude items past their TTL time manually
    see https://docs.amazonaws.cn/en_us/amazondynamodb/latest/developerguide/howitworks
    -ttl.html
    """
    test_data = [
        {
            "active": True,
            "actor": "mediumblue",
            "code": "YsSu4iAztUXm",
            "expiry_date": 1578304800,  # 06/01/2020 @ 10:00am (UTC)
            "generated_date": "2019-05-25",
            "last_updated_date": "2019-05-25",
            "dob": "1960-06-05",
            "lpa": "drive_leading-edge_communities",
        },
    ]
    code = None
    key = {
        "lpa": "drive_leading-edge_communities",
        "actor": "mediumblue",
    }

    expected_result = None
    expected_result_count = 0
    expected_logger_message = "LPA/actor does not exist in database"
    return (
        test_data,
        code,
        key,
        expected_result,
        expected_result_count,
        expected_logger_message,
    )


@case_name("Get codes by code that is past TTL")
def case_get_codes_12() -> CaseData:
    """
    TTL rows are not removed immediately, to be sure you are not returning any expired
    rows in a query you should exclude items past their TTL time manually
    see https://docs.amazonaws.cn/en_us/amazondynamodb/latest/developerguide/howitworks
    -ttl.html
    """
    test_data = [
        {
            "active": True,
            "actor": "mediumblue",
            "code": "YsSu4iAztUXm",
            "expiry_date": 1578304800,  # 06/01/2020 @ 10:00am (UTC)
            "generated_date": "2019-05-25",
            "last_updated_date": "2019-05-25",
            "dob": "1960-06-05",
            "lpa": "drive_leading-edge_communities",
        },
    ]
    code = "YsSu4iAztUXm"
    key = None

    expected_result = None
    expected_result_count = 0
    expected_logger_message = "Code does not exist in database"

    return (
        test_data,
        code,
        key,
        expected_result,
        expected_result_count,
        expected_logger_message,
    )
