import unittest
from unittest.mock import patch, Mock
import json
from Implementierung.ExceptionPackage.MatFlowException import UserExistsException, InternalException
from Implementierung.HardwareAdministration.Server import Server
from Implementierung.FrontendAPI.api import app
from Implementierung.FrontendAPI.api import FrontendAPI
from Implementierung.FrontendAPI import keys
from Implementierung.UserAdministration.User import User
from Implementierung.workflow.frontend_version import FrontendVersion
from Implementierung.workflow.parameter_change import ParameterChange
from Implementierung.workflow.version_number import VersionNumber


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
        self.failed_dict = {keys.status_code_name: InternalException("Server not found").get_status_code()}

    def test_getServer_called_1(self):
        with patch.object(FrontendAPI.hardware_controller.__class__, 'getServer', return_value=self.server) \
                as mock_method:
            self.app.get('get_server_details')
            # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
            assert mock_method.call_count > 0

    def test_getServer_called_2(self):
        with patch.object(FrontendAPI.hardware_controller.__class__, 'getServer', return_value=self.server):
            with patch.object(Server, 'encode_server',
                              return_value=self.expected_dict_server) as mock_method_2:

                self.app.get('get_server_details')
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method_2.call_count > 0

    def test_get_server_response_fail(self):
        with patch.object(FrontendAPI.hardware_controller.__class__, 'getServer',
                          side_effect=InternalException("Server not found")):
            with patch.object(Server, 'encode_server',
                              return_value=self.expected_dict_server):
                got = self.app.get('get_server_details')
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(self.failed_dict, retrieved_json)

    def test_getServer_response(self):
        with patch.object(FrontendAPI.hardware_controller.__class__, 'getServer', return_value=self.server):
            got = self.app.get('get_server_details')
            # content not relevant, Nils has to test this
            retrieved_json = json.loads(got.get_data())
            self.expected_dict_server.update(success_response)
            # get rid of python native data types
            expected_response = json.loads(json.dumps(self.expected_dict_server))
            self.assertEqual(retrieved_json, expected_response)

    def test_setServer_called_1(self):
        with patch.object(FrontendAPI.hardware_controller.__class__, 'setServer') as mock_method:
            self.app.put('set_server_details', json=json.dumps(self.expected_dict_server))
            # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
            assert mock_method.call_count > 0

    def test_setServer_called_2(self):
        with patch.object(FrontendAPI.hardware_controller.__class__, 'setServer'):
            with patch.object(Server, 'extract_server',
                              return_value=self.server) as mock_method_2:
                self.app.put('set_server_details', json=json.dumps(self.expected_dict_server))
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method_2.call_count > 0

    def test_set_server_response_fail(self):
        with patch.object(FrontendAPI.hardware_controller.__class__, 'setServer',
                          side_effect=InternalException("Server not valid")):
            with patch.object(Server, 'extract_server',
                              return_value=self.server):
                got = self.app.put('set_server_details', json=self.expected_dict_server)
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(self.failed_dict, retrieved_json)

    def test_setServer_response(self):
        with patch.object(FrontendAPI.hardware_controller.__class__, 'setServer'):
            with patch.object(Server, 'extract_server',
                              return_value=self.server):
                got = self.app.put('set_server_details', json=self.expected_dict_server)
                retrieved_json = json.loads(got.get_data())
                # get rid of python native data types
                self.assertEqual(retrieved_json, success_response)


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
        self.failed_dict = {keys.status_code_name: UserExistsException("scooby not found").get_status_code()}

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
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                self.assertEqual(retrieved_json, success_response)

    def test_set_user_response_fail(self):
        with patch.object(User, 'extract_user', return_value=self.user):
            with patch.object(FrontendAPI.user_controller.__class__, 'overrideUser',
                              side_effect=UserExistsException("scooby not found")):
                got = self.app.put('set_user_details', json=json.dumps(self.expected_dict_user_1))
                retrieved_json: dict = json.loads(got.get_data())
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
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
                              side_effect=UserExistsException("scooby not found")):
                got = self.app.delete('delete_user', json=json.dumps(self.expected_dict_user_1))
                retrieved_json: dict = json.loads(got.get_data())
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                self.assertEqual(retrieved_json, self.failed_dict)

    def test_delete_user_response_valid(self):
        with patch.object(User, 'extract_user', return_value=self.user):
            with patch.object(FrontendAPI.user_controller.__class__, 'deleteUser'):
                got = self.app.delete('delete_user', json=json.dumps(self.expected_dict_user_1))
                retrieved_json: dict = json.loads(got.get_data())
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                self.assertEqual(retrieved_json, success_response)


class WorkflowInstanceTest(unittest.TestCase):

    def setUp(self) -> None:
        self.frontendVersion1 = Mock()
        self.frontendVersion1.version_note_name = "scooby"
        self.frontendVersion1.version_number_name = "doo"
        self.frontendVersion1.frontend_versions_changes = "None"
        self.return_version_dict = {"he": "Scooby"}
        self.frontendVersion2 = Mock()
        self.app = app.test_client()
        self.failed_dict = {keys.status_code_name: InternalException("whoops").get_status_code()}

    def test_get_wf_instance_versions_call_wf_manager(self):
        with patch.object(FrontendAPI.workflow_manager.__class__, 'get_versions_from_workflow_instance',
                          return_value=[self.frontendVersion1, self.frontendVersion2]) as mock_method:
            with patch.object(self.frontendVersion1, 'encode_version', return_value=dict()):
                with patch.object(self.frontendVersion2, 'encode_version', return_value=dict()):
                    self.app.get('get_wf_instance_versions',
                                 json=json.dumps({keys.workflow_instance_name: "bla"}))
                    # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called()
                    # throws error
                    assert mock_method.call_count > 0

    def test_get_wf_instance_versions_call_encode_1(self):
        with patch.object(FrontendAPI.workflow_manager.__class__, 'get_versions_from_workflow_instance',
                          return_value=[self.frontendVersion1, self.frontendVersion2]):
            with patch.object(self.frontendVersion1, 'encode_version', return_value=dict()) as mock_method_2:
                with patch.object(self.frontendVersion2, 'encode_version', return_value=dict()):
                    self.app.get('get_wf_instance_versions',
                                 json=json.dumps({keys.workflow_instance_name: "bla"}))
                    # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called()
                    # throws error
                    assert mock_method_2.call_count > 0

    def test_get_wf_instance_versions_call_encode_2(self):
        with patch.object(FrontendAPI.workflow_manager.__class__, 'get_versions_from_workflow_instance',
                          return_value=[self.frontendVersion1, self.frontendVersion2]):
            with patch.object(self.frontendVersion1, 'encode_version', return_value=dict()):
                with patch.object(self.frontendVersion2, 'encode_version', return_value=dict()) as mock_method_3:
                    self.app.get('get_wf_instance_versions',
                                 json=json.dumps({keys.workflow_instance_name: "bla"}))
                    # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called()
                    # throws error
                    assert mock_method_3.call_count > 0

    def test_get_wf_instance_versions_response_fail(self):
        with patch.object(FrontendAPI.workflow_manager.__class__, 'get_versions_from_workflow_instance',
                          side_effect=InternalException("whoops")):
            with patch.object(self.frontendVersion1, 'encode_version', return_value=dict()):
                with patch.object(self.frontendVersion2, 'encode_version', return_value=dict()):
                    got = self.app.get('get_wf_instance_versions',
                                       json=json.dumps({keys.workflow_instance_name: "bla"}))
                    retrieved_json: dict = json.loads(got.get_data())
                    # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called()
                    # throws error
                    self.assertEqual(retrieved_json, self.failed_dict)

    def test_get_wf_instance_versions_response_valid(self):
        # we need a real version here; all other attempts have failed due to circular dependencies (of mocks)
        version: FrontendVersion = FrontendVersion(VersionNumber("1"), "bla",
                                                   [ParameterChange("bla", "bla", "bla", "bla", "bla")])
        with patch.object(FrontendAPI.workflow_manager.__class__, 'get_versions_from_workflow_instance',
             return_value=[version, version]):
            got = self.app.get('get_wf_instance_versions',
                               json=json.dumps({keys.workflow_instance_name: "bla"}))
            print(got)
            retrieved_json: dict = json.loads(got.get_data())
            expected_dict: dict = json.loads(json.dumps({keys.versions_name: [version.encode_version(),
                                                                              version.encode_version()]}))
            expected_dict.update(success_response)
            # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
            self.assertEqual(retrieved_json, expected_dict)

    def test_replace_wf_instance_active_versions_call_wf_manager(self):
        with patch.object(FrontendAPI.workflow_manager.__class__, 'set_active_version_through_number') as mock_method:
            self.app.put('replace_wf_instance_active_version',
                         json=json.dumps({keys.workflow_instance_name: "bla", keys.version_number_name: "scooby"}))
            # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
            assert mock_method.call_count > 0

    def test_replace_wf_instance_active_versions_fail(self):
        with patch.object(FrontendAPI.workflow_manager.__class__, 'set_active_version_through_number',
                          side_effect=InternalException("oops")):
            got = self.app.put('replace_wf_instance_active_version',
                               json=json.dumps({keys.workflow_instance_name: "bla",
                                                keys.version_number_name: "scooby"}))
            retrieved_json: dict = json.loads(got.get_data())
            # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
            self.assertEqual(retrieved_json, self.failed_dict)

    def test_replace_wf_instance_active_versions_valid(self):
        with patch.object(FrontendAPI.workflow_manager.__class__, 'set_active_version_through_number'):
            got = self.app.put('replace_wf_instance_active_version',
                               json=json.dumps({keys.workflow_instance_name: "bla",
                                                keys.version_number_name: "scooby"}))
            retrieved_json: dict = json.loads(got.get_data())
            # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
            self.assertEqual(retrieved_json, self.failed_dict)


if __name__ == '__main__':
    unittest.main()
