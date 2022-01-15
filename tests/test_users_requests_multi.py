import logging
import time

import grequests
import pytest
import json
from app_lib import common_lib

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestMultiRequestsUser:
    headers = {"Content-type": "application/json"}
    timeout_in_secs = 60

    @pytest.mark.parametrize("code, expected_code, expected_output, requester",
                             [({"code": "1000+1"}, 200, "1001", "user_1"),
                              ({"code": "1000+2"}, 200, "1002", "user_2"),
                              ({"code": "1000+3"}, 200, "1003", "user_3"),
                              ({"code": "1000+4"}, 200, "1004", "user_4"),
                              ({"code": "1000+5"}, 200, "1005", "user_5")])
    def test_all_valid_users_submit_code_and_check_complete_status(self, environment_details, user_details, code, expected_code, expected_output, requester):
        TestMultiRequestsUser.test_all_valid_users_submit_code_and_check_complete_status.__doc__ = '::'.join(["Verify sending requests from valid users", requester])
        payload = json.dumps(code)
        base_url = common_lib.get_base_url(environment_details)
        token = user_details[requester]['auth']
        logger.info(f"User[{requester}] :: {token}")
        self.headers.update({'Authorization': 'Basic %s' % token})

        res = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
        assert res.status_code == expected_code
        code_id = res.json().get("id")
        logger.info(f"code_id={code_id}")

        res = common_lib.get_groovy_code_status_by_id(environment_details, base_url, self.headers, code_id)
        assert res.status_code == expected_code

        status_url = common_lib.generate_endpoint(environment_details, base_url, "status", code_id)
        res = common_lib.wait_until_status(status_url, self.headers, self.timeout_in_secs, common_lib.CodeStatus.COMPLETED.value)
        expected = common_lib.generate_groovy_code_status_template(code_id, common_lib.CodeStatus.COMPLETED.value,
                                                                   result=expected_output)
        assert res.json() == json.loads(expected)

    @pytest.mark.parametrize("number_of_requests, expected_code", [(2,200), (10,200)])
    def test_multiple_requests_and_check_complete_status(self, environment_details, user_details, number_of_requests, expected_code):
        TestMultiRequestsUser.test_multiple_requests_and_check_complete_status.__doc__ = f"Verifying sending multiple requests \"{number_of_requests}\" by same user to check parallel execution"
        base_url = common_lib.get_base_url(environment_details)
        token = user_details['user_2']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})

        all_status, status_ok = [], []
        requests_list = []
        initial_digit = common_lib.generate_random_number(4)
        submit_url = common_lib.generate_endpoint(environment_details, base_url, "submit", None)
        for index in range(number_of_requests):
            requests_list.append(grequests.post(submit_url, headers=self.headers, json={"code": "(%s)*(%s)" % (initial_digit, str(index))}))

        res_list = grequests.map(requests_list)
        time.sleep(3)

        for res in res_list:
            all_status.append(res.status_code)
            if res.status_code == expected_code:
                status_ok.append([res_list.index(res), res.json()['id']])
            else:
                logger.info(f"The request {res.json()} has status code as {res.status_code}")

        assert all_status.count(expected_code) == number_of_requests

        for value in status_ok:
            index = value[0]
            code_id = value[1]
            res = common_lib.get_groovy_code_status_by_id(environment_details, base_url, self.headers, code_id)
            assert res.status_code == expected_code
            expected = common_lib.generate_groovy_code_status_template(code_id, common_lib.CodeStatus.COMPLETED.value,
                                                                       result=str(int(initial_digit) * index))
            assert res.json() == json.loads(expected)

    @pytest.mark.parametrize("number_of_requests, expected_code", [(5, 200)])
    def test_multiple_user_requests_and_check_status(self, environment_details, user_details, number_of_requests, expected_code):
        TestMultiRequestsUser.test_multiple_user_requests_and_check_status.__doc__ = f"Verifying sending \"{number_of_requests}\" requests by different users to check parallel execution"

        base_url = common_lib.get_base_url(environment_details)

        all_status, status_ok = [], []
        requests_list = []
        initial_digit = common_lib.generate_random_number(4)
        submit_url = common_lib.generate_endpoint(environment_details, base_url, "submit", None)
        for index in range(1, (number_of_requests+1)):
            token = user_details[f'user_{index}']['auth']
            self.headers.update({'Authorization': 'Basic %s' % token})
            requests_list.append(grequests.post(submit_url, headers=self.headers, json={"code": "(%s)*(%s)" % (initial_digit, str(index))}))

        res_list = grequests.map(requests_list)
        time.sleep(3)

        for res in res_list:
            all_status.append(res.status_code)
            if res.status_code == expected_code:
                status_ok.append([res_list.index(res), res.json()['id']])
            else:
                logger.info(f"The request {res.json()} has status code as {res.status_code}")

        assert all_status.count(expected_code) == number_of_requests

        for value in status_ok:
            index = value[0]
            code_id = value[1]
            res = common_lib.get_groovy_code_status_by_id(environment_details, base_url, self.headers, code_id)
            assert res.status_code == expected_code
            expected = common_lib.generate_groovy_code_status_template(code_id, common_lib.CodeStatus.COMPLETED.value,
                                                                       result=str(int(initial_digit) * index))
            assert res.json() == json.loads(expected)

    @pytest.mark.parametrize("expected_code", [200])
    def test_blocking_requests_and_check_complete_status(self, environment_details, user_details, expected_code):
        TestMultiRequestsUser.test_blocking_requests_and_check_complete_status.__doc__ = "Verify if service handles requests when have some blocking requests and some normal requests"

        base_url = common_lib.get_base_url(environment_details)
        token = user_details['user_3']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})

        all_status, status_ok, blocking_requests = [], [], []

        number_of_blocking_requests = 2
        for i in range(number_of_blocking_requests):
            payload = '{"code": "while(true){sleep(1000); %s}"}' % i
            res = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
            logger.info(f"Response of request #{i} is : {res.json()}")
            blocking_requests.append(res.status_code)
        assert all_status.count(expected_code) == number_of_blocking_requests

        number_of_normal_requests = 6
        initial_digit = common_lib.generate_random_number(3)
        for i in range(number_of_normal_requests):
            payload = '{"code": "%s+%s"}' % (initial_digit,str(i))
            res = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
            all_status.append(res.status_code)
            if res.status_code == expected_code:
                status_ok.append(res.json()['id'])
                status_ok.append([i, res.json()['id']])

        assert all_status.count(expected_code) == number_of_normal_requests

        for value in status_ok:
            index = value[0]
            code_id = value[1]
            res = common_lib.get_groovy_code_status_by_id(environment_details, base_url, self.headers, code_id)
            expected = common_lib.generate_groovy_code_status_template(code_id, common_lib.CodeStatus.COMPLETED.value, result=str(index + int(initial_digit)))
            assert res.json() == json.loads(expected)