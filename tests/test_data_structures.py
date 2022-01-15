import logging
import pytest
import json
from app_lib import common_lib

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestDataStructures:
    headers = {"Content-type": "application/json"}
    timeout_in_secs = 60

    @pytest.mark.parametrize("test_name, code, expected_code, expected_output",
                             [("Verify array creation and adding item to array", {"code": "def arr = [1, 2, 3]; arr.add(4); return arr;"}, 200, "[1, 2, 3, 4]"),
                              ("Verify removing item from array", {"code": "def arr = [1, 2, 3, 4]; arr.remove(1); return arr;"}, 200, "[1, 3, 4]"),
                              ("Verify catching and returning custom exception message for array", {"code": "try {def arr = new int[1]; arr[9] = 3; return arr;} catch(Exception ex) {return 'custom exception occurred';}"}, 200, "custom exception occurred")])
    def test_array_submit_code_and_check_complete_status(self, environment_details, user_details, test_name, code, expected_code, expected_output):
        TestDataStructures.test_array_submit_code_and_check_complete_status.__doc__ = test_name

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
        expected = common_lib.generate_groovy_code_status_template(code_id, common_lib.CodeStatus.COMPLETED.value,
                                                                   result=expected_output)
        assert res.json() == json.loads(expected)

    @pytest.mark.parametrize("test_name, code, expected_code, expected_output",
                             [("Verify generating ArrayIndexOutOfBoundsException exception for array", {"code": "def arr = new int[1];arr[3] = 4; return arr;"}, 200, "ArrayIndexOutOfBoundsException")])
    def test_array_submit_code_and_check_failed_status(self, environment_details, user_details, test_name, code, expected_code,
                                                       expected_output):
        TestDataStructures.test_array_submit_code_and_check_failed_status.__doc__ = test_name
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
        res = common_lib.wait_until_status(status_url, self.headers, self.timeout_in_secs, common_lib.CodeStatus.FAILED.value)
        # expected = common_lib.generate_groovy_code_status_template(code_id, common_lib.CodeStatus.COMPLETED.value, result=expected_output)
        # assert res.json() == json.loads(expected)
        res_data = res.json()
        assert res_data['status'] == 'FAILED'
        assert expected_output in res_data['result']

    @pytest.mark.parametrize("test_name, code, expected_code, expected_output",
                             [("Verify creating map and adding item to map", {"code": "def map = ['FirstName' : 'Rohit', 'LastName' : 'Tupe']; map.put('City','Pune'); return map;"}, 200, "{FirstName=Rohit, LastName=Tupe, City=Pune}"),
                              ("Verify replacing item value from map", {"code": "def map = ['FirstName' : 'Rohit', 'LastName' : 'Tupe', 'State' : 'Maharashtra']; map['State']='MH'; return map;"}, 200, "{FirstName=Rohit, LastName=Tupe, State=MH}"),
                              ("Verify removing item from map", {"code": "def map = ['FirstName' : 'Rohit', 'LastName' : 'Tupe', 'City' : 'Pune']; map.remove('City'); return map;"}, 200, "{FirstName=Rohit, LastName=Tupe}"),
                              ("Verify creating map and displaying only values from map", {"code": "def map = ['FirstName' : 'Rohit', 'LastName' : 'Tupe']; return map.values();"}, 200, "[Rohit, Tupe]")])
    def test_map_submit_code_and_check_complete_status(self, environment_details, user_details, test_name, code, expected_code,
                                                       expected_output):
        TestDataStructures.test_map_submit_code_and_check_complete_status.__doc__ = test_name
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
        expected = common_lib.generate_groovy_code_status_template(code_id, common_lib.CodeStatus.COMPLETED.value,
                                                                   result=expected_output)
        assert res.json() == json.loads(expected)

    @pytest.mark.parametrize("test_name, code, expected_code, expected_output",
                             [("Verify submitting closure block with no arguments", {"code": "def fun = {println 'Hello World'; return 'closure block called'}; fun.call();"}, 200, "closure block called"),
                              ("Verify submitting closure block with arguments", {"code": "def str1 = 'Coder'; def closureWithOneArg = {str -> str.toUpperCase()+str1}; closureWithOneArg.call('groovy');"}, 200, "GROOVYCoder")])
    def test_closure_block_submit_code_and_check_complete_status(self, environment_details, user_details, test_name, code,
                                                                 expected_code, expected_output):
        TestDataStructures.test_closure_block_submit_code_and_check_complete_status.__doc__ = test_name
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
        expected = common_lib.generate_groovy_code_status_template(code_id, common_lib.CodeStatus.COMPLETED.value,
                                                                   result=expected_output)
        assert res.json() == json.loads(expected)
