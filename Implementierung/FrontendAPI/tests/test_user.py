import json
import unittest
from unittest.mock import patch
from Implementierung.FrontendAPI.api import app, FrontendAPI
from Implementierung.FrontendAPI import keys
from Implementierung.ExceptionPackage.MatFlowException import InternalException
from Implementierung.UserAdministration.User import User
success_response: dict = {"statusCode": 607}


class UserTest(unittest.TestCase):

    """ All user calls are tested. We do not test anything further behind the api, that's why we mock most of the
    additional backend. Note that privilege checking is not yet added"""
    def setUp(self) -> None:
        self.app = app.test_client()
        self.user: User = User(username='scooby', status="accepted", privilege="admin", password="scooby_dooby_doo")

        self.expected_dict_user_1: dict = {keys.user_name: "scooby", keys.user_status_name: "accepted",
                                           keys.user_privilege_name: "admin", keys.password_name: "scooby_dooby_doo"}

        self.expected_dict_user_2: dict = {keys.user_name: "shaggy", keys.user_status_name: "accepted",
                                           keys.user_privilege_name: "user", keys.password_name: "jinkies"}
        self.all_users: dict = {keys.all_users: [self.expected_dict_user_1, self.expected_dict_user_2]}
        self.failed_dict = {keys.status_code_name: InternalException("scooby not found").get_status_code()}

    def test_get_all_users_call(self):
        with patch.object(FrontendAPI.user_controller.__class__, 'getAllUsersAndDetails',
                          return_value=self.all_users) as mock_method:
            self.app.get('get_all_users_and_details')
            # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
            assert mock_method.call_count > 0
            # no exceptions possible

    def test_getAllUsersAndDetails_response(self):
        # we only get an array of users
        with patch.object(FrontendAPI.user_controller.__class__, 'getAllUsersAndDetails',
                          return_value=self.all_users[keys.all_users]):
            got = self.app.get('get_all_users_and_details')
            # content not relevant, Nils has to test this
            retrieved_json = json.loads(got.get_data())
            self.all_users.update(success_response)
            # get rid of python native data types
            expected_response = json.loads(json.dumps(self.all_users))
            self.assertEqual(retrieved_json, expected_response)

    def test_set_user_call_1(self):
        with patch.object(User, 'extract_user', return_value=self.user) as mock_method:
            with patch.object(FrontendAPI.user_controller.__class__, 'overrideUser'):
                self.app.put('set_user_details', json=json.dumps(self.expected_dict_user_1))
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method.call_count > 0

    def test_set_user_call_2(self):
        with patch.object(User, 'extract_user', return_value=self.user):
            with patch.object(FrontendAPI.user_controller.__class__, 'overrideUser') as mock_method_2:
                self.app.put('set_user_details', json=json.dumps(self.expected_dict_user_1))
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method_2.call_count > 0

    def test_set_user_response_valid(self):
        with patch.object(User, 'extract_user', return_value=self.user):
            with patch.object(FrontendAPI.user_controller.__class__, 'overrideUser'):
                got = self.app.put('set_user_details', json=json.dumps(self.expected_dict_user_1))
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(retrieved_json, success_response)

    def test_set_user_response_fail(self):
        with patch.object(User, 'extract_user', return_value=self.user):
            with patch.object(FrontendAPI.user_controller.__class__, 'overrideUser',
                              side_effect=InternalException("scooby not found")):
                got = self.app.put('set_user_details', json=json.dumps(self.expected_dict_user_1))
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(retrieved_json, self.failed_dict)

    def test_delete_user_call_1(self):
        with patch.object(User, 'extract_user', return_value=self.user) as mock_method:
            with patch.object(FrontendAPI.user_controller.__class__, 'deleteUser'):
                self.app.delete('delete_user', json=json.dumps(self.expected_dict_user_1))
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method.call_count > 0

    def test_delete_user_call_2(self):
        with patch.object(User, 'extract_user', return_value=self.user):
            with patch.object(FrontendAPI.user_controller.__class__, 'deleteUser') as mock_method_2:
                self.app.delete('delete_user', json=json.dumps(self.expected_dict_user_1))
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method_2.call_count > 0

    def test_delete_user_response_fail(self):
        with patch.object(User, 'extract_user', return_value=self.user):
            with patch.object(FrontendAPI.user_controller.__class__, 'deleteUser',
                              side_effect=InternalException("scooby not found")):
                got = self.app.delete('delete_user', json=json.dumps(self.expected_dict_user_1))
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(retrieved_json, self.failed_dict)

    def test_delete_user_response_valid(self):
        with patch.object(User, 'extract_user', return_value=self.user):
            with patch.object(FrontendAPI.user_controller.__class__, 'deleteUser'):
                got = self.app.delete('delete_user', json=json.dumps(self.expected_dict_user_1))
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(retrieved_json, success_response)

    def test_verify_login_call_login(self):
        with patch.object(FrontendAPI.user_controller.__class__, "loginUser") as mock_method:
            self.app.get('verify_login', json=json.dumps({keys.user_name: "scooby", keys.password_name: "doo"}))
            assert mock_method.call_count > 0

    def test_verify_login_response_fail(self):
        with patch.object(FrontendAPI.user_controller.__class__, "loginUser", side_effect=InternalException("oops")):
            got = self.app.get('verify_login', json=json.dumps({keys.user_name: "scooby", keys.password_name: "doo"}))
            retrieved_json: dict = json.loads(got.get_data())
            expected_dict: dict = self.failed_dict
            self.assertEqual(retrieved_json, expected_dict)

    def test_verify_login_response_valid(self):
        with patch.object(FrontendAPI.user_controller.__class__, "loginUser"):
            got = self.app.get('verify_login', json=json.dumps({keys.user_name: "scooby", keys.password_name: "doo"}))
            retrieved_json: dict = json.loads(got.get_data())
            expected_dict: dict = success_response
            self.assertEqual(retrieved_json, expected_dict)

    def test_register_user_call_create_user(self):
        with patch.object(FrontendAPI.user_controller.__class__, "createUser") as mock_method:
            self.app.post('register_user', json=json.dumps({keys.user_name: "scooby", keys.password_name: "doo",
                                                            keys.repeat_password_name: "doo"}))
            assert mock_method.call_count > 0

    def test_register_user_response_fail(self):
        with patch.object(FrontendAPI.user_controller.__class__, "createUser", side_effect=InternalException("oops")):
            got = self.app.post('register_user', json=json.dumps({keys.user_name: "scooby", keys.password_name: "doo",
                                                            keys.repeat_password_name: "doo"}))
            retrieved_json: dict = json.loads(got.get_data())
            self.assertEqual(self.failed_dict, retrieved_json)

    def test_register_user_response_valid(self):
        with patch.object(FrontendAPI.user_controller.__class__, "createUser"):
            got = self.app.post('register_user', json=json.dumps({keys.user_name: "scooby", keys.password_name: "doo",
                                                                  keys.repeat_password_name: "doo"}))
            retrieved_json: dict = json.loads(got.get_data())
            self.assertEqual(success_response, retrieved_json)


if __name__ == '__main__':
    unittest.main()
