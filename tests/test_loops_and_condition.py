import logging
import pytest
import json
from app_lib import common_lib

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestLoopsAndConditions:
    headers = {"Content-type": "application/json"}
    timeout_in_secs = 60

    @pytest.mark.parametrize("test_name, code, expected_code, expected_output",
                             [("Verify while loop without return statement", {"code": "int cnt = 0; while(cnt<5) {cnt++;  cnt;}"}, 200, "1"),
                              ("Verify while loop with return statement", {"code": "int counter = 0; while(counter<5) {counter++; return counter;}"}, 200, "1")])
    def test_while_loop_submit_code_and_check_complete_status(self, environment_details, user_details, test_name, code, expected_code, expected_output):
        TestLoopsAndConditions.test_while_loop_submit_code_and_check_complete_status.__doc__ = test_name
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
                             [("Verify for loop with if and return statement", {"code": "int[] arr = [0,1,2,3]; for(int i in arr) {if(i == 2) return i;}"}, 200, "2")])
    def test_for_loop_submit_code_and_check_complete_status(self, environment_details, user_details, test_name, code, expected_code,
                                                       expected_output):
        TestLoopsAndConditions.test_for_loop_submit_code_and_check_complete_status.__doc__ = test_name
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
                             [("Verify if-else with continue statement", {"code": "int[] arr_1 = [0,1,2,3]; for(int i in arr_1) {if(i == 0) continue; else return i; }"}, 200, "1"),
                              ("Verify if-else with return statement", {"code": "int x=2; if(x<1) return x; else return 'hello world';"}, 200, "hello world")])
    def test_if_else_submit_code_and_check_complete_status(self, environment_details, user_details, test_name, code, expected_code, expected_output):
        TestLoopsAndConditions.test_if_else_submit_code_and_check_complete_status.__doc__ = test_name
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
                             [("Verify switch case statement", {"code": "int x = 3; switch(x) {case 1: return 1;break; case 2: return 2; break; case 3:return 3; break;case 4:return 4; break; default:return 'default'; break;}"}, 200, "3")])
    def test_switch_case_submit_code_and_check_complete_status(self, environment_details, user_details, test_name, code, expected_code, expected_output):
        TestLoopsAndConditions.test_switch_case_submit_code_and_check_complete_status.__doc__ = test_name
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
