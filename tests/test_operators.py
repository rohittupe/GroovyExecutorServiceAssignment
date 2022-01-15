import logging
import pytest
import json
from app_lib import common_lib

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestOperators:
    headers = {"Content-type": "application/json"}
    timeout_in_secs = 90

    @pytest.mark.parametrize("test_name, code, expected_code, expected_output",
                             [("Addition", {"code": "def x = 1, y = 3; x+y;"}, 200, "4"),
                              ("Subtraction", {"code": "def x = 2, y = 1; x-y;"}, 200, "1"),
                              ("Multiplication", {"code": "def x = 3, y = 1; x*y;"}, 200, "3"),
                              ("Division", {"code": "def x = 6, y = 3; x/y;"}, 200, "2"),
                              ("Remainder", {"code": "def x = 10, y = 5; x%y;"}, 200, "0"),
                              ("Power", {"code": "def x = 3, y = 2; x**y;"}, 200, "9"),
                              ("Increment", {"code": "def x = 2; x++; x;"}, 200, "3"),
                              ("Decrement", {"code": "def x = 2; x--; x;"}, 200, "1")])
    def test_arithmetic_submit_code_and_check_complete_status(self, environment_details, user_details, test_name, code, expected_code, expected_output):
        TestOperators.test_arithmetic_submit_code_and_check_complete_status.__doc__ = f"Verify arithmetic operator - {test_name}"
        payload = json.dumps(code)
        base_url = common_lib.get_base_url(environment_details)
        token = user_details['user_1']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})

        res = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
        assert res.status_code == expected_code
        code_id = res.json().get("id")
        logger.info(f"code_id={code_id}")

        res = common_lib.get_groovy_code_status_by_id(environment_details, base_url, self.headers, code_id)
        assert res.status_code == expected_code
        logger.info(f"Initial get request output: {res.json()}")
        status_url = common_lib.generate_endpoint(environment_details, base_url, "status", code_id)
        res = common_lib.wait_until_status(status_url, self.headers, self.timeout_in_secs, common_lib.CodeStatus.COMPLETED.value)
        assert res
        expected = common_lib.generate_groovy_code_status_template(code_id, common_lib.CodeStatus.COMPLETED.value,
                                                                   result=expected_output)
        assert res.json() == json.loads(expected)

    @pytest.mark.parametrize("test_name, code, expected_code, expected_output",
                             [("Addition", {"code": "def x = 2; x+=3;"}, 200, "5"),
                              ("Subtraction", {"code": "def x = 3; x-=2;"}, 200, "1"),
                              ("Multiplication", {"code": "def x = 1; x*=3;"}, 200, "3"),
                              ("Division", {"code": "def x = 4; x/=2;"}, 200, "2"),
                              ("Remainder", {"code": "def x = 6; x%=2;"}, 200, "0")])
    def test_assignment_submit_code_and_check_complete_status(self, environment_details, user_details, test_name, code, expected_code, expected_output):
        TestOperators.test_assignment_submit_code_and_check_complete_status.__doc__ = f"Verify assignment operator - {test_name}"
        payload = json.dumps(code)
        base_url = common_lib.get_base_url(environment_details)
        token = user_details['user_1']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})

        res = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
        assert res.status_code == expected_code
        code_id = res.json().get("id")
        logger.info(f"code_id={code_id}")

        res = common_lib.get_groovy_code_status_by_id(environment_details, base_url, self.headers, code_id)
        assert res.status_code == expected_code

        status_url = common_lib.generate_endpoint(environment_details, base_url, "status", code_id)
        res = common_lib.wait_until_status(status_url, self.headers, self.timeout_in_secs, common_lib.CodeStatus.COMPLETED.value)
        assert res
        expected = common_lib.generate_groovy_code_status_template(code_id, common_lib.CodeStatus.COMPLETED.value,
                                                                   result=expected_output)
        assert res.json() == json.loads(expected)

    @pytest.mark.parametrize("test_name, code, expected_code, expected_output",
                             [("0 AND 0", {"code": "0 & 0"}, 200, "0"),
                              ("0 AND 1", {"code": "0 & 1"}, 200, "0"),
                              ("1 AND 0", {"code": "1 & 0"}, 200, "0"),
                              ("1 AND 1", {"code": "1 & 1"}, 200, "1"),
                              ("0 OR 0", {"code": "0 | 0"}, 200, "0"),
                              ("0 OR 1", {"code": "0 | 1"}, 200, "1"),
                              ("1 OR 0", {"code": "1 | 0"}, 200, "1"),
                              ("1 OR 1", {"code": "1 | 1"}, 200, "1"),
                              ("0 XOR 0", {"code": "0 ^ 0"}, 200, "0"),
                              ("0 XOR 1", {"code": "0 ^ 1"}, 200, "1"),
                              ("1 XOR 0", {"code": "1 ^ 0"}, 200, "1"),
                              ("1 XOR 1", {"code": "1 ^ 1"}, 200, "0"),
                              ("Negation Negative Number", {"code": "~-2"}, 200, "1"),
                              ("Negation Positive Number", {"code": "~2"}, 200, "-3")])
    def test_bitwise_submit_code_and_check_complete_status(self, environment_details, user_details, test_name, code, expected_code, expected_output):
        TestOperators.test_bitwise_submit_code_and_check_complete_status.__doc__ = f"Verify bitwise operator - {test_name}"
        payload = json.dumps(code)
        base_url = common_lib.get_base_url(environment_details)
        token = user_details['user_1']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})

        res = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
        assert res.status_code == expected_code
        code_id = res.json().get("id")
        logger.info(f"code_id={code_id}")

        res = common_lib.get_groovy_code_status_by_id(environment_details, base_url, self.headers, code_id)
        assert res.status_code == expected_code

        status_url = common_lib.generate_endpoint(environment_details, base_url, "status", code_id)
        res = common_lib.wait_until_status(status_url, self.headers, self.timeout_in_secs, common_lib.CodeStatus.COMPLETED.value)
        assert res
        expected = common_lib.generate_groovy_code_status_template(code_id, common_lib.CodeStatus.COMPLETED.value,
                                                                   result=expected_output)
        assert res.json() == json.loads(expected)

    @pytest.mark.parametrize("test_name, code, expected_code, expected_output",
                             [("Equal - true", {"code": "def x = 1; x==1;"}, 200, "true"),
                              ("Equal - false", {"code": "def x = 1; x==2;"}, 200, "false"),
                              ("Not Equal - true", {"code": "def x = 1; x!=2;"}, 200, "true"),
                              ("Not Equal - false", {"code": "def x = 1; x!=1;"}, 200, "false"),
                              ("Less than or equal - true", {"code": "def x = 1; x<=2;"}, 200, "true"),
                              ("Less than or equal - false", {"code": "def x = 3; x<=2;"}, 200, "false"),
                              ("Greater than or equal - true", {"code": "def x = 2; x>=1;"}, 200, "true"),
                              ("Greater than or equal - false", {"code": "def x = 1; x>=2;"}, 200, "false")])
    def test_relational_submit_code_and_check_complete_status(self, environment_details, user_details, test_name, code, expected_code, expected_output):
        TestOperators.test_relational_submit_code_and_check_complete_status.__doc__ = f"Verify relational operator - {test_name}"
        payload = json.dumps(code)
        base_url = common_lib.get_base_url(environment_details)
        token = user_details['user_1']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})

        res = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
        assert res.status_code == expected_code
        code_id = res.json().get("id")
        logger.info(f"code_id={code_id}")

        res = common_lib.get_groovy_code_status_by_id(environment_details, base_url, self.headers, code_id)
        assert res.status_code == expected_code

        status_url = common_lib.generate_endpoint(environment_details, base_url, "status", code_id)
        res = common_lib.wait_until_status(status_url, self.headers, self.timeout_in_secs, common_lib.CodeStatus.COMPLETED.value)
        assert res
        expected = common_lib.generate_groovy_code_status_template(code_id, common_lib.CodeStatus.COMPLETED.value,
                                                                   result=expected_output)
        assert res.json() == json.loads(expected)

    @pytest.mark.parametrize("test_name, code, expected_code, expected_output",
                             [("false AND false", {"code": "false && false"}, 200, "false"),
                              ("true AND false", {"code": "true && false"}, 200, "false"),
                              ("false AND true", {"code": "false && true"}, 200, "false"),
                              ("true AND true", {"code": "true && true"}, 200, "true"),
                              ("false OR false", {"code": "false || false"}, 200, "false"),
                              ("true OR false", {"code": "true || false"}, 200, "true"),
                              ("false OR true", {"code": "false || true"}, 200, "true"),
                              ("true OR true", {"code": "true || true"}, 200, "true"),
                              ("NOT true", {"code": "!true"}, 200, "false"),
                              ("NOT false", {"code": "!false"}, 200, "true")])
    def test_logical_submit_code_and_check_complete_status(self, environment_details, user_details, test_name, code, expected_code, expected_output):
        TestOperators.test_logical_submit_code_and_check_complete_status.__doc__ = f"Verify logical operator - {test_name}"
        payload = json.dumps(code)
        base_url = common_lib.get_base_url(environment_details)
        token = user_details['user_1']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})

        res = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
        assert res.status_code == expected_code
        code_id = res.json().get("id")
        logger.info(f"code_id={code_id}")

        res = common_lib.get_groovy_code_status_by_id(environment_details, base_url, self.headers, code_id)
        assert res.status_code == expected_code

        status_url = common_lib.generate_endpoint(environment_details, base_url, "status", code_id)
        res = common_lib.wait_until_status(status_url, self.headers, self.timeout_in_secs, common_lib.CodeStatus.COMPLETED.value)
        assert res
        expected = common_lib.generate_groovy_code_status_template(code_id, common_lib.CodeStatus.COMPLETED.value,
                                                                   result=expected_output)
        assert res.json() == json.loads(expected)
