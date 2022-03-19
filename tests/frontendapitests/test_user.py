import base64
import json
import unittest
from copy import deepcopy
from unittest.mock import patch, Mock
from matflow.database.DatabaseTable import DatabaseTable

with patch.object(DatabaseTable, "get_instance", return_value=""):
    from matflow.frontendapi.api import app, FrontendAPI
    from matflow.frontendapi import keys
from matflow.exceptionpackage.MatFlowException import InternalException
from matflow.useradministration.User import User

success_response: dict = {"statusCode": 607}


class UserTest(unittest.TestCase):

    """All user calls are tested. We do not test anything further behind the api, that's why we mock most of the
    additional backend. Note that privilege checking is not yet added"""

    def setUp(self) -> None:
        self.app = app.test_client()
        self.user = Mock()
        self.expected_dict_user_1: dict = {
            keys.user_name: "scooby",
            keys.user_status_name: "accepted",
            keys.user_privilege_name: "admin",
            keys.password_name: "scooby_dooby_doo",
        }

        self.expected_dict_user_2: dict = {
            keys.user_name: "shaggy",
            keys.user_status_name: "accepted",
            keys.user_privilege_name: "user",
            keys.password_name: "jinkies",
        }
        self.all_users: dict = {
            "total_entries": 2,
            "users": [
                {
                    "active": True,
                    "changed_on": "2022-02-24T21:16:07.771595",
                    "created_on": "2022-02-24T21:16:07.771470",
                    "email": "airflowadmin@example.com",
                    "fail_login_count": 0,
                    "first_name": "Airflow",
                    "last_login": "2022-02-25T14:40:36.356283",
                    "last_name": "Admin",
                    "login_count": 183,
                    "roles": [{"name": "Admin"}],
                    "username": "airflow",
                },
                {
                    "active": True,
                    "changed_on": "2022-02-25T08:49:46.339749",
                    "created_on": "2022-02-25T08:49:46.339308",
                    "email": ".",
                    "fail_login_count": 0,
                    "first_name": ".",
                    "last_login": "2022-02-25T08:58:08.301726",
                    "last_name": ".",
                    "login_count": 3,
                    "roles": [{"name": "Admin"}],
                    "username": "first_user",
                },
            ],
        }

        self.all_users_response = json.loads(
            json.dumps(
                {
                    keys.all_users: [
                        {
                            keys.user_name: "airflow",
                            keys.user_status_name: True,
                            keys.user_privilege_name: "Admin",
                        },
                        {
                            keys.user_name: "first_user",
                            keys.user_status_name: True,
                            keys.user_privilege_name: "Admin",
                        },
                    ]
                }
            )
        )
        self.failed_dict = {
            keys.status_code_name: InternalException(
                "scooby not found"
            ).get_status_code(),
            "error_message": "whoops",
        }
        to_be_encoded = json.dumps({"username": "test", "password": "test"}).encode(
            "utf-8"
        )
        self.headers = {
            "Authorization": "Basic {}".format(
                base64.b64encode(to_be_encoded).decode("utf-8")
            )
        }

    def test_get_all_users_call(self):
        with patch.object(
            FrontendAPI.user_controller.__class__,
            "getAllUsersAndDetails",
            return_value=self.all_users,
        ) as mock_method:
            self.app.get("get_all_users_and_details", headers=self.headers)
            # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
            assert mock_method.call_count > 0
            # no exceptions possible

    def test_getAllUsersAndDetails_response(self):
        # we only get an array of users
        with patch.object(
            FrontendAPI.user_controller.__class__,
            "getAllUsersAndDetails",
            return_value=self.all_users,
        ):
            got = self.app.get("get_all_users_and_details", headers=self.headers)
            # content not relevant, Nils has to test this
            retrieved_json = json.loads(got.get_data())
            expected_response: dict = deepcopy(self.all_users_response)
            expected_response.update(success_response)
            # get rid of python native data types
            expected_response = json.loads(json.dumps(expected_response))
            self.assertEqual(retrieved_json, expected_response)

    def test_set_user_call_1(self):
        with patch.object(User, "extract_user", return_value=self.user) as mock_method:
            with patch.object(FrontendAPI.user_controller.__class__, "overrideUser"):
                self.app.put(
                    "set_user_details",
                    json=json.dumps(self.expected_dict_user_1),
                    headers=self.headers,
                )
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method.call_count > 0

    def test_set_user_call_2(self):
        with patch.object(User, "extract_user", return_value=self.user):
            with patch.object(
                FrontendAPI.user_controller.__class__, "overrideUser"
            ) as mock_method_2:
                self.app.put(
                    "set_user_details",
                    json=json.dumps(self.expected_dict_user_1),
                    headers=self.headers,
                )
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method_2.call_count > 0

    def test_set_user_response_valid(self):
        with patch.object(User, "extract_user", return_value=self.user):
            with patch.object(FrontendAPI.user_controller.__class__, "overrideUser"):
                got = self.app.put(
                    "set_user_details",
                    json=json.dumps(self.expected_dict_user_1),
                    headers=self.headers,
                )
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(retrieved_json, success_response)

    def test_set_user_response_fail(self):
        with patch.object(User, "extract_user", return_value=self.user):
            with patch.object(
                FrontendAPI.user_controller.__class__,
                "overrideUser",
                side_effect=InternalException("whoops"),
            ):
                got = self.app.put(
                    "set_user_details",
                    json=json.dumps(self.expected_dict_user_1),
                    headers=self.headers,
                )
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(retrieved_json, self.failed_dict)

    def test_delete_user_call_1(self):
        with patch.object(User, "extract_user", return_value=self.user) as mock_method:
            with patch.object(FrontendAPI.user_controller.__class__, "deleteUser"):
                self.app.delete(
                    "delete_user",
                    json=json.dumps(self.expected_dict_user_1),
                    headers=self.headers,
                )
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method.call_count > 0

    def test_delete_user_call_2(self):
        with patch.object(User, "extract_user", return_value=self.user):
            with patch.object(
                FrontendAPI.user_controller.__class__, "deleteUser"
            ) as mock_method_2:
                self.app.delete(
                    "delete_user",
                    json=json.dumps(self.expected_dict_user_1),
                    headers=self.headers,
                )
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method_2.call_count > 0

    def test_delete_user_response_fail(self):
        with patch.object(User, "extract_user", return_value=self.user):
            with patch.object(
                FrontendAPI.user_controller.__class__,
                "deleteUser",
                side_effect=InternalException("whoops"),
            ):
                got = self.app.delete(
                    "delete_user",
                    json=json.dumps(self.expected_dict_user_1),
                    headers=self.headers,
                )
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(retrieved_json, self.failed_dict)

    def test_delete_user_response_valid(self):
        with patch.object(User, "extract_user", return_value=self.user):
            with patch.object(FrontendAPI.user_controller.__class__, "deleteUser"):
                got = self.app.delete(
                    "delete_user",
                    json=json.dumps(self.expected_dict_user_1),
                    headers=self.headers,
                )
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(retrieved_json, success_response)

    @unittest.skip("Login deprecated")
    def test_verify_login_call_login(self):
        with patch.object(
            FrontendAPI.user_controller.__class__, "loginUser"
        ) as mock_method:
            self.app.get(
                "verify_login",
                json=json.dumps({keys.user_name: "scooby", keys.password_name: "doo"}),
            )
            assert mock_method.call_count > 0

    @unittest.skip("Login deprecated")
    def test_verify_login_response_fail(self):
        with patch.object(
            FrontendAPI.user_controller.__class__,
            "loginUser",
            side_effect=InternalException("oops"),
        ):
            got = self.app.get(
                "verify_login",
                json=json.dumps({keys.user_name: "scooby", keys.password_name: "doo"}),
            )
            retrieved_json: dict = json.loads(got.get_data())
            self.assertEqual(retrieved_json, self.failed_dict)

    @unittest.skip("Login deprecated")
    def test_verify_login_response_valid(self):
        with patch.object(FrontendAPI.user_controller.__class__, "loginUser"):
            got = self.app.get(
                "verify_login",
                json=json.dumps({keys.user_name: "scooby", keys.password_name: "doo"}),
            )
            retrieved_json: dict = json.loads(got.get_data())
            self.assertEqual(retrieved_json, success_response)

    def test_register_user_call_create_user(self):
        with patch.object(
            FrontendAPI.user_controller.__class__, "createUser"
        ) as mock_method:
            self.app.post(
                "register_user",
                json=json.dumps(
                    {
                        keys.user_name: "scooby",
                        keys.password_name: "doo",
                        keys.repeat_password_name: "doo",
                    }
                ),
                headers=self.headers,
            )
            assert mock_method.call_count > 0

    def test_register_user_response_fail(self):
        with patch.object(
            FrontendAPI.user_controller.__class__,
            "createUser",
            side_effect=InternalException("whoops"),
        ):
            got = self.app.post(
                "register_user",
                json=json.dumps(
                    {
                        keys.user_name: "scooby",
                        keys.password_name: "doo",
                        keys.repeat_password_name: "doo",
                    }
                ),
                headers=self.headers,
            )
            retrieved_json: dict = json.loads(got.get_data())
            self.assertEqual(self.failed_dict, retrieved_json)

    def test_register_user_response_valid(self):
        with patch.object(FrontendAPI.user_controller.__class__, "createUser"):
            got = self.app.post(
                "register_user",
                json=json.dumps(
                    {
                        keys.user_name: "scooby",
                        keys.password_name: "doo",
                        keys.repeat_password_name: "doo",
                    }
                ),
                headers=self.headers,
            )
            retrieved_json: dict = json.loads(got.get_data())
            self.assertEqual(success_response, retrieved_json)


if __name__ == "__main__":
    unittest.main()
