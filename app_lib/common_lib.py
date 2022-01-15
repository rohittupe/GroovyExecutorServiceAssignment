import logging
import string
import time
from datetime import datetime, timedelta
from enum import Enum
import random
import requests
from schema import Schema, Or, Regex

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

groovy_code_status_template = '''{"id": "%s", "status": "%s", "result": "%s"}'''

status_schema = Schema({
    "id": str,
    "status": str,
    "result": Or(str, None)
})

submit_schema = Schema({
    "id": str
})

error_schema = Schema({
    "timestamp": Regex("[0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2}T[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}.[0-9]{1,3}\+[0-9]{1,2}:[0-9]{1,2}"),
    "status": int,
    "error": str,
    "message": str,
    "path": str
})

key_authorization = 'Authorization'


class CodeStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


def generate_random_string(length=1):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_random_number(length=1):
    range_start = 10 ** (length - 1)
    range_end = (10 ** length) - 1
    return random.randint(range_start, range_end)


# def wait_until_status_complete(url, headers, timeout_in_seconds):
#     current_time = datetime.now()
#     print(f"current_time={current_time}")
#     end_time = current_time + timedelta(seconds=timeout_in_seconds)
#     while end_time >= current_time:
#         print("in while")
#         res = requests.get(url=url, headers=headers)
#         if res.json().get('status') == "COMPLETED":
#             return res
#         current_time = datetime.now()
#         print(f"in while current_time={current_time}")
#     return None

def wait_until_status(url, headers, timeout_in_seconds, status=CodeStatus.COMPLETED.value):
    logger.info(f"Waiting for max {timeout_in_seconds} seconds for status \"{status}\"...")
    current_time = datetime.now()
    #print(f"current_time={current_time}")
    end_time = current_time + timedelta(seconds=timeout_in_seconds)
    while end_time >= current_time:
        #print("in while")
        res = requests.get(url=url, headers=headers)
        res_status = res.json().get('status')
        if res_status == status:
            return res
        elif res_status != status and res_status in ['FAILED']:
            return res
        current_time = datetime.now()
        time.sleep(1)
        #print(f"in while current_time={current_time}")
    return None


def get_base_url(environment_details):
    url = f"{environment_details['host']}:{environment_details['port']}"
    return url


def generate_endpoint(environment_details, base_url, type, code_id=None):
    if "submit" in type:
        url = f"{base_url}{environment_details['submit']}"
    else:
        if code_id:
            url = f"{base_url}{environment_details['status']}?id={code_id}"
        else:
            url = f"{base_url}{environment_details['status']}"
    return url


def generate_groovy_code_status_template(code_id, status=CodeStatus.COMPLETED.value, result=None):
    template = groovy_code_status_template % (code_id, status, result)
    return template


def submit_groovy_code(environment_details, url, headers, payload):
    # submit_url = f"{url}{environment_details['submit']}"
    submit_url = generate_endpoint(environment_details, url, "submit", None)
    print(f"submit_url={submit_url}")
    res = requests.post(url=submit_url, headers=headers, data=payload)
    return res


def get_groovy_code_status_by_id(environment_details, url, headers, code_id):
    # status_url = f"{url}{environment_details['status']}?id={code_id}"
    status_url = generate_endpoint(environment_details, url, "status", code_id)
    res = requests.get(url=status_url, headers=headers)
    return res


def remove_from_headers(headers, key):
    if headers and key in headers.keys():
        headers.pop(key)
    return headers
