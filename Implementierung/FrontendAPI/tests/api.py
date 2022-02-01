import unittest
from unittest.mock import patch
import json

from Implementierung.ExceptionPackage.MatFlowException import UserExistsException, MatFlowException, InternalException
from Implementierung.HardwareAdministration.Server import Server
from Implementierung.FrontendAPI.api import app
from Implementierung.FrontendAPI.api import FrontendAPI
from Implementierung.FrontendAPI import keys
from Implementierung.UserAdministration.User import User


def create_json(dictionary: dict) -> str:
    return json.dumps(dictionary)


success_response: dict = {"statusCode": 607}


class APITest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()

    def test_api_reachability(self):
        posted = self.app.post('/')
        retrieved_json: dict = json.loads(posted.get_data())
        self.assertEqual(success_response, retrieved_json)



class ServerTest(unittest.TestCase):

    """
    Both server calls get and set are tested. The calls within in the functions are tested whether they've been called
    In get_server we compare a server object we expect with the one we got(with mock) to make sure the api is working
    """
    def setUp(self) -> None:
        self.app = app.test_client()
        self.expected_dict_server: dict = {keys.server_name: "server", keys.server_status_name: "online",
                                           keys.server_address_name: "127.0.0.1", keys.container_limit_name: 4,
                                           keys.server_resources_name: [('ha', 'ha')],
                                           keys.selected_for_execution_name: True}
        self.server: Server = Server("server",
                          "127.0.0.1", "online", 4, True, [('ha', 'ha')])
        self.failed_dict= {keys.status_code_name: InternalException("Server not found").get_status_code()}


    def test_getServer_called_1(self):
        with patch.object(FrontendAPI.hardware_controller.__class__, 'getServer', return_value= self.server) as mock_method:
            got = self.app.get('get_server_details')
            retrieved_json: dict = json.loads(got.get_data())
            # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
            assert mock_method.call_count > 0

    def test_getServer_called_2(self):
        with patch.object(FrontendAPI.hardware_controller.__class__, 'getServer', return_value=self.server) as mock_method:
            with patch.object(Server, 'encode_server',
                              return_value=self.expected_dict_server) as mock_method_2:

                got = self.app.get('get_server_details')
                retrieved_json: dict = json.loads(got.get_data())
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method_2.call_count > 0

    def test_get_server_response_fail(self):
        with patch.object(FrontendAPI.hardware_controller.__class__, 'getServer',
                          side_effect=InternalException("Server not found")) as mock_method:
            with patch.object(Server, 'encode_server',
                              return_value=self.expected_dict_server) as mock_method_2:
                got = self.app.get('get_server_details')
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(self.failed_dict, retrieved_json)

    def test_getServer_response(self):
        with patch.object(FrontendAPI.hardware_controller.__class__, 'getServer', return_value=self.server) as mock_method:
            got = self.app.get('get_server_details')
            # content not relevant, Nils has to test this
            retrieved_json = json.loads(got.get_data())
            self.expected_dict_server.update(success_response)
            # get rid of python native data types
            expected_response = json.loads(json.dumps(self.expected_dict_server))
            self.assertEqual(retrieved_json, expected_response)

    def test_setServer_called_1(self):
        with patch.object(FrontendAPI.hardware_controller.__class__, 'setServer') as mock_method:
            got = self.app.put('set_server_details', json=json.dumps(self.expected_dict_server))
            # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
            assert mock_method.call_count > 0

    def test_setServer_called_2(self):
        with patch.object(FrontendAPI.hardware_controller.__class__, 'setServer') as mock_method_1:
            with patch.object(Server, 'extract_server',
                              return_value=self.server) as mock_method_2:
                got = self.app.put('set_server_details', json=json.dumps(self.expected_dict_server))
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method_2.call_count > 0

    def test_set_server_response_fail(self):
        with patch.object(FrontendAPI.hardware_controller.__class__, 'setServer',
                          side_effect=InternalException("Server not valid")) as mock_method:
            with patch.object(Server, 'extract_server',
                              return_value=self.server) as mock_method_2:
                got = self.app.put('set_server_details', json= self.expected_dict_server)
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(self.failed_dict, retrieved_json)

    def test_setServer_response(self):
        with patch.object(FrontendAPI.hardware_controller.__class__, 'setServer') as mock_method:
            with patch.object(Server, 'extract_server',
                              return_value=self.server) as mock_method_2:
                got = self.app.put('set_server_details', json=self.expected_dict_server)
                retrieved_json = json.loads(got.get_data())
                # get rid of python native data types
                self.assertEqual(retrieved_json, success_response)


class UserTest(unittest.TestCase):

    """ All user calls are tested. We do not tests anything further behind the api, that's why we mock most of the
    additional backend. Note that privilege checking is not yet added"""
    def setUp(self) -> None:
        self.app = app.test_client()
        self.user: User = User(username='scooby', status="accepted", privilege="admin", password="scooby_dooby_doo")

        self.expected_dict_user_1: dict = {keys.user_name: "scooby", keys.user_status_name: "accepted", keys.user_privilege_name:
                                   "admin", keys.password_name: "scooby_dooby_doo"}

        self.expected_dict_user_2: dict = {keys.user_name: "shaggy", keys.user_status_name: "accepted",
                                           keys.user_privilege_name: "user", keys.password_name: "jinkies"}
        self.all_users: dict = {keys.all_users: [self.expected_dict_user_1, self.expected_dict_user_2]}
        self.failed_dict = {keys.status_code_name: UserExistsException("scooby not found").get_status_code()}

    def test_get_all_users_call(self):
        with patch.object(FrontendAPI.user_controller.__class__, 'getAllUsersAndDetails',
                          return_value= self.all_users) as mock_method:
            got = self.app.get('get_all_users_and_details')
            retrieved_json: dict = json.loads(got.get_data())
            # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
            assert mock_method.call_count > 0
            # no exceptions possible

    def test_getAllUsersAndDetails_response(self):
        # we only get an array of users
        with patch.object(FrontendAPI.user_controller.__class__, 'getAllUsersAndDetails',
                          return_value=self.all_users[keys.all_users]) as mock_method:
            got = self.app.get('get_all_users_and_details')
            # content not relevant, Nils has to test this
            retrieved_json = json.loads(got.get_data())
            self.all_users.update(success_response)
            # get rid of python native data types
            expected_response = json.loads(json.dumps(self.all_users))
            self.assertEqual(retrieved_json, expected_response)

    def test_set_user_call_1(self):
        with patch.object(User, 'extract_user',return_value= self.user) as mock_method:
            with patch.object(FrontendAPI.user_controller.__class__, 'overrideUser') as mock_method_2:
                got = self.app.put('set_user_details', json= json.dumps(self.expected_dict_user_1))
                retrieved_json: dict = json.loads(got.get_data())
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method.call_count > 0

    def test_set_user_call_2(self):
        with patch.object(User, 'extract_user',return_value= self.user) as mock_method:
            with patch.object(FrontendAPI.user_controller.__class__, 'overrideUser') as mock_method_2:
                got = self.app.put('set_user_details', json= json.dumps(self.expected_dict_user_1))
                retrieved_json: dict = json.loads(got.get_data())
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method_2.call_count > 0

    def test_set_user_response_valid(self):
        with patch.object(User, 'extract_user',return_value= self.user) as mock_method:
            with patch.object(FrontendAPI.user_controller.__class__, 'overrideUser') as mock_method_2:
                got = self.app.put('set_user_details', json= json.dumps(self.expected_dict_user_1))
                retrieved_json: dict = json.loads(got.get_data())
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                self.assertEqual(retrieved_json, success_response)

    def test_set_user_response_fail(self):
        with patch.object(User, 'extract_user',return_value= self.user) as mock_method:
            with patch.object(FrontendAPI.user_controller.__class__, 'overrideUser',
                              side_effect= UserExistsException("scooby not found")) as mock_method:
                got = self.app.put('set_user_details', json= json.dumps(self.expected_dict_user_1))
                retrieved_json: dict = json.loads(got.get_data())
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                self.assertEqual(retrieved_json, self.failed_dict)



    def test_delete_user_call_1(self):
        with patch.object(User, 'extract_user',return_value= self.user) as mock_method:
            with patch.object(FrontendAPI.user_controller.__class__, 'deleteUser') as mock_method_2:
                got = self.app.delete('delete_user', json= json.dumps(self.expected_dict_user_1))
                retrieved_json: dict = json.loads(got.get_data())
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method.call_count > 0

    def test_delete_user_call_2(self):
        with patch.object(User, 'extract_user',return_value= self.user) as mock_method:
            with patch.object(FrontendAPI.user_controller.__class__, 'deleteUser') as mock_method_2:
                got = self.app.delete('delete_user', json= json.dumps(self.expected_dict_user_1))
                retrieved_json: dict = json.loads(got.get_data())
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method_2.call_count > 0

    def test_delete_user_response_fail(self):
        with patch.object(User, 'extract_user',return_value= self.user) as mock_method:
            with patch.object(FrontendAPI.user_controller.__class__, 'deleteUser',
                              side_effect= UserExistsException("scooby not found")) as mock_method:
                got = self.app.delete('delete_user', json= json.dumps(self.expected_dict_user_1))
                retrieved_json: dict = json.loads(got.get_data())
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                self.assertEqual(retrieved_json, self.failed_dict)

    def test_delete_user_response_valid(self):
        with patch.object(User, 'extract_user',return_value= self.user) as mock_method:
            with patch.object(FrontendAPI.user_controller.__class__, 'deleteUser') as mock_method_2:
                got = self.app.delete('delete_user', json= json.dumps(self.expected_dict_user_1))
                retrieved_json: dict = json.loads(got.get_data())
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                self.assertEqual(retrieved_json, success_response)



if __name__ == '__main__':
    unittest.main()
