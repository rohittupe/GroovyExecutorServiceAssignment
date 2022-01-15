import logging
import pytest
import json
from app_lib import common_lib

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestAuthentication:
    headers = {"Content-type": "application/json"}
    timeout_in_secs = 60

    @pytest.mark.parametrize("test_name, code, expected_code, expected_output", [("Verify valid authentication", {"code": "100+100"}, 200, "200")])
    def test_valid_auth_and_check_status(self, environment_details, user_details, test_name, code, expected_code, expected_output):
        TestAuthentication.test_valid_auth_and_check_status.__doc__ = test_name
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

    @pytest.mark.parametrize("test_name, code, expected_code",
                             [('Verify submit service without authentication','{ "code": "100+101" }', 401)])
    def test_no_auth_to_submit(self, environment_details, user_details, test_name, code, expected_code):
        TestAuthentication.test_no_auth_to_submit.__doc__ = test_name
        payload = json.dumps(code)
        base_url = common_lib.get_base_url(environment_details)
        headers = common_lib.remove_from_headers(self.headers, common_lib.key_authorization)
        res = common_lib.submit_groovy_code(environment_details, base_url, headers, payload)
        assert res.status_code == expected_code

    @pytest.mark.parametrize("test_name, code, expected_code, expected_code_2",
                             [("Verify status service without authentication", {"code": "101+100"}, 200, 401)])
    def test_no_auth_to_status(self, environment_details, user_details, test_name, code, expected_code, expected_code_2):
        TestAuthentication.test_no_auth_to_status.__doc__ = test_name
        payload = json.dumps(code)
        base_url = common_lib.get_base_url(environment_details)
        token = user_details['user_1']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})

        res = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
        assert res.status_code == expected_code
        code_id = res.json().get("id")
        logger.info(f"code_id={code_id}")

        headers = common_lib.remove_from_headers(self.headers, 'Authorization')
        res = common_lib.get_groovy_code_status_by_id(environment_details, base_url, headers, code_id)
        assert res.status_code == expected_code_2

    @pytest.mark.parametrize("test_name, code, expected_code",
                             [("Verify submit service with invalid user", '{ "code": "111+112" }', 401)])
    def test_invalid_auth_to_submit(self, environment_details, user_details, test_name, code, expected_code):
        TestAuthentication.test_invalid_auth_to_submit.__doc__ = test_name
        payload = json.dumps(code)
        base_url = common_lib.get_base_url(environment_details)
        token = user_details['invalid_user_1']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})
        res = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
        assert res.status_code == expected_code

    @pytest.mark.parametrize("test_name, code, expected_code, expected_code_2",
                             [("Verify status service with invalid user", {"code": "120+100"}, 200, 401)])
    def test_invalid_auth_to_status(self, environment_details, user_details, test_name, code, expected_code, expected_code_2):
        TestAuthentication.test_invalid_auth_to_status.__doc__ = test_name
        payload = json.dumps(code)
        base_url = common_lib.get_base_url(environment_details)
        token = user_details['user_1']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})

        res = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
        assert res.status_code == expected_code
        code_id = res.json().get("id")
        logger.info(f"code_id={code_id}")

        token = user_details['invalid_user_1']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})
        res = common_lib.get_groovy_code_status_by_id(environment_details, base_url, self.headers, code_id)
        assert res.status_code == expected_code_2

    @pytest.mark.parametrize("test_name, code, expected_code",
                             [("Verify accessing submit service with valid username from one user and password of other user", {"code": "121+122"}, 401)])
    def test_valid_different_username_and_password_auth_to_submit(self, environment_details, user_details, test_name, code, expected_code):
        TestAuthentication.test_valid_different_username_and_password_auth_to_submit.__doc__ = test_name
        payload = json.dumps(code)
        base_url = common_lib.get_base_url(environment_details)
        token = user_details['mismatch_user_1']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})
        res = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
        assert res.status_code == expected_code

    @pytest.mark.parametrize("test_name, code, expected_code, expected_code_2",
                             [("Verify accessing status service with valid username from one user and password of other user", {"code": "103+100"}, 200, 401)])
    def test_valid_different_username_and_password_auth_to_status(self, environment_details, user_details, test_name, code, expected_code, expected_code_2):
        TestAuthentication.test_valid_different_username_and_password_auth_to_status.__doc__ = test_name
        payload = json.dumps(code)
        base_url = common_lib.get_base_url(environment_details)
        token = user_details['user_1']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})

        res = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
        assert res.status_code == expected_code
        code_id = res.json().get("id")
        logger.info(f"code_id={code_id}")

        token = user_details['mismatch_user_1']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})
        res = common_lib.get_groovy_code_status_by_id(environment_details, base_url, self.headers, code_id)
        assert res.status_code == expected_code_2

    @pytest.mark.parametrize("test_name, code, expected_code_post, expected_code_get",
                             [("Verify accessing submit service with one user and status with other user", {"code": "122+123"}, 200, 401)])
    def test_cross_auth_submit_and_status_check(self, environment_details, user_details, test_name, code, expected_code_post, expected_code_get):
        # Submit the code using one user and request details using get from different user
        TestAuthentication.test_cross_auth_submit_and_status_check.__doc__ = test_name
        payload = json.dumps(code)
        base_url = common_lib.get_base_url(environment_details)
        token = user_details['user_1']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token})

        res = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload)
        assert res.status_code == expected_code_post
        code_id = res.json().get("id")
        logger.info(f"code_id={code_id}")

        token_1 = user_details['user_2']['auth']
        self.headers.update({'Authorization': 'Basic %s' % token_1})
        res = common_lib.get_groovy_code_status_by_id(environment_details, base_url, self.headers, code_id)
        assert res.status_code == expected_code_get

    @pytest.mark.parametrize("test_name, code, expected_code, code_2, expected_code_2",
                             [("Verify accessing submit with and without auth", {"code": "131+132"}, 200, {"code": "140+140"}, 401)])
    def test_with_and_without_auth_submit(self, environment_details, user_details, test_name, code, expected_code, code_2, expected_code_2):
        TestAuthentication.test_with_and_without_auth_submit.__doc__ = test_name
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

        # status_url = common_lib.generate_endpoint(environment_details, base_url, "status", code_id)
        # res = common_lib.wait_until_status(status_url, self.headers, 120, common_lib.CodeStatus.COMPLETED.value)
        # expected = common_lib.generate_groovy_code_status_template(code_id, common_lib.CodeStatus.COMPLETED.value,
        #                                                            result=expected_output)
        # assert res.json() == json.loads(expected)

        payload_2 = json.dumps(code_2)
        self.headers.pop("Authorization")
        res_2 = common_lib.submit_groovy_code(environment_details, base_url, self.headers, payload_2)
        assert res_2.status_code == expected_code_2

    @pytest.mark.parametrize("test_name, code, expected_code, expected_code_2",
                              [("Verify accessing status with and without auth", {"code": "141+132"}, 200, 401)])
    def test_with_and_without_auth_status(self, environment_details, user_details, test_name, code, expected_code, expected_code_2):
        TestAuthentication.test_with_and_without_auth_status.__doc__ = test_name
        text = ''.join([common_lib.generate_random_string(3), common_lib.generate_random_string(2)])
        code = {"code": f"{text}"}
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

        headers = common_lib.remove_from_headers(self.headers, common_lib.key_authorization)
        res = common_lib.get_groovy_code_status_by_id(environment_details, base_url, headers, code_id)
        assert res.status_code == expected_code_2
