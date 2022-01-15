import logging
import pytest
import json
from faker import Faker
from app_lib import common_lib

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestDefaults:
    headers = {"Content-type": "application/json"}
    timeout_in_secs = 60

    @pytest.mark.parametrize("test_name, code, expected_code",
                             [("Verify submitting null code", '{ "code": null }', 400),
                              ("Verify submitting code with no payload", '{}', 400), ])
    def test_submit_null_code_and_check_status(self, environment_details, user_details, test_name, code,
                                               expected_code):
        TestDefaults.test_submit_null_code_and_check_status.__doc__ = test_name
        payload = json.dumps(code)
        base_url = common_lib.get_base_url(environment_details)
        token = user_details['user_1']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})
        res = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
        assert res.status_code == expected_code

    @pytest.mark.parametrize("test_name, code, expected_code, expected_output",
                             [("Verify submitting an empty string code", {"code": ""}, 200, "null"),
                              ("Verify submitting code with null as string", {"code": "null"}, 200, "null")])
    def test_submit_empty_code_and_check_status(self, environment_details, user_details, test_name, code, expected_code,
                                                expected_output):
        TestDefaults.test_submit_empty_code_and_check_status.__doc__ = test_name
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
                             [("Verify submitting number addition code", {"code": "21+22"}, 200, "43"),
                              ("Verify submitting decimal number addition code", {"code": "1.1+1.1"}, 200, "2.2"),
                              ("Verify submitting only number code", {"code": "1234"}, 200, "1234"),
                              ("Verify submitting only string code", {"code": "xyz"}, 200, "xyz"),
                              ("Verify submitting code with println function", {"code": "println 'hello'"}, 200, "null"),
                              ("Verify submitting code with return statement", {"code": "return 'hello'"}, 200, "hello"),
                              ("Verify submitting code with range", {"code": "def range = 1..5; range.get(1);"}, 200, "2"),
                              ("Verify submitting string concat code", {"code": "'Hello' + 'World'"}, 200, "HelloWorld")])
    def test_submit_code_and_check_complete_status(self, environment_details, user_details, test_name, code, expected_code,
                                                   expected_output):
        TestDefaults.test_submit_code_and_check_complete_status.__doc__ = test_name
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
        expected_status = common_lib.CodeStatus.COMPLETED.value
        res = common_lib.wait_until_status(status_url, self.headers, self.timeout_in_secs, expected_status)
        expected = common_lib.generate_groovy_code_status_template(code_id, expected_status, result=expected_output)
        assert res
        assert res.json() == json.loads(expected)

    @pytest.mark.parametrize("test_name, code, expected_code, expected_output",
                             [("Verify class and main method submission without return statement", {"code": "class World {static void main(String[] args) {System.out.println('hi');}}"}, 200, "null"),
                              ("Verify class and user defined method submission while returning variable", {"code": "class Tester {static void main(String[] args) {Tester.test();}; static String test(){def x = 'testing'; x;}}"}, 200, "testing"),
                              ("Verify class and user defined method submission with return statement", {"code": "class Coder {static void main(String[] args) {Coder.develop();}; static String develop(){return 'developing';}}"}, 200, "developing")])
    def test_submit_methods_class_code_and_check_complete_status(self, environment_details, user_details, test_name, code, expected_code, expected_output):
        TestDefaults.test_submit_methods_class_code_and_check_complete_status.__doc__ = test_name
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
        res_data = res.json()
        assert res_data['status'] == 'COMPLETED' and expected_output in res_data['result']

    @pytest.mark.parametrize("test_name, code, expected_code, expected_output",
                             [("Verify invalid code submission results in execption with FAILED status", {"code": "$$"}, 200, "No such property"),
                              ("Verify class and a static method submission", {"code": "class Analyst {static String get_requirements(){return 'capturing';}}"}, 200, "MissingMethodExceptionNoStack")])
    def test_submit_invalid_code_and_check_failed_status(self, environment_details, user_details, test_name, code, expected_code,
                                                         expected_output):
        TestDefaults.test_submit_invalid_code_and_check_failed_status.__doc__ = test_name
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
        res_data = res.json()
        assert res_data['status'] == 'FAILED'
        assert expected_output in res_data['result']

    @pytest.mark.parametrize("test_name, code, expected_code",
                             [("Verify IN_PROGRESS status on code submission", {"code":"sleep(20000); 900+900;"}, 200,)])
    def test_submit_code_and_check_in_progress_status(self, environment_details, user_details, test_name, code, expected_code):
        TestDefaults.test_submit_code_and_check_in_progress_status.__doc__ = test_name
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
        res_data = res.json()
        assert res_data['status'] == 'IN_PROGRESS'

    @pytest.mark.parametrize("test_name, code, expected_code",
                             [("Verify submitting same code more than once should give same result", {"code": "31+32"}, 200)])
    def test_submit_same_code_twice_and_check_status(self, environment_details, user_details, test_name, code, expected_code):
        TestDefaults.test_submit_same_code_twice_and_check_status.__doc__ = test_name
        payload = json.dumps(code)
        base_url = common_lib.get_base_url(environment_details)
        token = user_details['user_1']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})

        res_1 = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
        assert res_1.status_code == expected_code

        res_2 = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
        assert res_2.status_code == expected_code

    @pytest.mark.parametrize("test_name, code_id, expected_code",
                             [("Verify status service with invalid id", None, 404)])
    def test_status_with_invalid_id(self, environment_details, user_details, test_name, code_id, expected_code):
        TestDefaults.test_status_with_invalid_id.__doc__ = test_name
        base_url = common_lib.get_base_url(environment_details)
        token = user_details['user_1']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})
        if not code_id:
            fake = Faker()
            code_id = fake.uuid4()
        #"7d5d2181-4b85-4bee-9a12-29c6328cdee56"
        res = common_lib.get_groovy_code_status_by_id(environment_details, base_url, self.headers, code_id)
        assert res.status_code == expected_code

    @pytest.mark.parametrize("test_name, code, expected_code",
                             [("Verify schema for submit response", {"code": "300+300"}, 200)])
    def test_submit_schema(self, environment_details, user_details, test_name, code, expected_code):
        TestDefaults.test_submit_schema.__doc__ = test_name
        payload = json.dumps(code)
        base_url = common_lib.get_base_url(environment_details)
        token = user_details['user_1']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})

        res = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
        assert res.status_code == expected_code
        common_lib.submit_schema.validate(res.json())

    @pytest.mark.parametrize("test_name, code, expected_code",
                             [("Verify schema for status response", {"code": "311+311"}, 200)])
    def test_status_schema(self, environment_details, user_details, test_name, code, expected_code):
        TestDefaults.test_status_schema.__doc__ = test_name
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
        common_lib.status_schema.validate(res.json())

    @pytest.mark.parametrize("test_name, code, expected_code",
                             [("Verify schema for error response", {"code": "'x'+'y'"}, 401)])
    def test_error_schema(self, environment_details, user_details, test_name, code, expected_code):
        TestDefaults.test_error_schema.__doc__ = test_name
        payload = json.dumps(code)
        base_url = common_lib.get_base_url(environment_details)
        headers = common_lib.remove_from_headers(self.headers, common_lib.key_authorization)
        res = common_lib.submit_groovy_code(environment_details, base_url, headers, payload)
        assert res.status_code == expected_code
        common_lib.error_schema.validate(res.json())

    @pytest.mark.parametrize("test_name, code, expected_code_post, expected_code_get",
                             [("Verify adding extra param to status request should not be successfull", {"code": "10000+2"}, 200, 404)])
    def test_additional_param_to_status(self, environment_details, user_details, test_name, code, expected_code_post, expected_code_get):
        TestDefaults.test_additional_param_to_status.__doc__ = test_name
        payload = json.dumps(code)
        base_url = common_lib.get_base_url(environment_details)
        token = user_details['user_1']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})

        res = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
        assert res.status_code == expected_code_post
        code_id = res.json().get("id")
        logger.info(f"code_id={code_id}")

        test = f'{code_id}&xyz=123'
        res = common_lib.get_groovy_code_status_by_id(environment_details, base_url, self.headers, test)
        assert res.status_code == expected_code_get