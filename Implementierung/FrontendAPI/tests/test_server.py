import json
import unittest
from copy import deepcopy
from unittest.mock import patch, Mock
from Implementierung.FrontendAPI.api import app, FrontendAPI
from Implementierung.FrontendAPI import keys
from Implementierung.ExceptionPackage.MatFlowException import InternalException

success_response: dict = {"statusCode": 607}


class ServerTest(unittest.TestCase):

    """
    Both server calls get and set are tested. The calls within in the functions are tested whether they've been called
    In get_server we compare a server object we expect with the one we got(with mock) to make sure the api is working
    """

    def setUp(self) -> None:
        self.app = app.test_client()
        self.expected_dict_server: dict = {
            keys.server_name: "server",
            keys.server_status_name: "online",
            keys.server_address_name: "127.0.0.1",
            keys.container_limit_name: 4,
            keys.server_resources_name: [("ha", "ha")],
            keys.selected_for_execution_name: True,
        }
        self.server = Mock()
        self.failed_dict = {
            keys.status_code_name: InternalException(
                "Server not found"
            ).get_status_code()
        }

    def test_getServer_called_1(self):
        with patch.object(
            FrontendAPI.hardware_controller.__class__,
            "getServer",
            return_value=self.server,
        ) as mock_method:
            with patch.object(
                self.server, "encode_server", return_value=self.expected_dict_server
            ):
                self.app.get("get_server_details")
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method.call_count > 0

    def test_getServer_called_2(self):
        with patch.object(
            FrontendAPI.hardware_controller.__class__,
            "getServer",
            return_value=self.server,
        ):
            with patch.object(
                self.server, "encode_server", return_value=self.expected_dict_server
            ) as mock_method_2:

                self.app.get("get_server_details")
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method_2.call_count > 0

    def test_get_server_response_fail(self):
        with patch.object(
            FrontendAPI.hardware_controller.__class__,
            "getServer",
            side_effect=InternalException("Server not found"),
        ):
            with patch.object(
                self.server, "encode_server", return_value=self.expected_dict_server
            ):
                got = self.app.get("get_server_details")
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(self.failed_dict, retrieved_json)

    def test_getServer_response(self):
        with patch.object(
            FrontendAPI.hardware_controller.__class__,
            "getServer",
            return_value=self.server,
        ):
            with patch.object(
                self.server, "encode_server", return_value=self.expected_dict_server
            ):
                got = self.app.get("get_server_details")
                # content not relevant, Nils has to test this
                retrieved_json = json.loads(got.get_data())
                expected_dict: dict = deepcopy(self.expected_dict_server)
                expected_dict.update(success_response)
                # get rid of python native data types
                expected_response = json.loads(json.dumps(expected_dict))
                self.assertEqual(retrieved_json, expected_response)

    def test_setServer_called_1(self):
        with patch.object(
            FrontendAPI.hardware_controller.__class__, "setServer"
        ) as mock_method:
            with patch.object(self.server, "extract_server", return_value=self.server):
                self.app.put(
                    "set_server_details", json=json.dumps(self.expected_dict_server)
                )
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method.call_count > 0

    def test_setServer_called_2(self):
        with patch.object(FrontendAPI.hardware_controller.__class__, "setServer"):
            with patch.object(
                self.server, "extract_server", return_value=self.server
            ) as mock_method_2:
                self.app.put(
                    "set_server_details", json=json.dumps(self.expected_dict_server)
                )
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method_2.call_count > 0

    def test_set_server_response_fail(self):
        with patch.object(
            FrontendAPI.hardware_controller.__class__,
            "setServer",
            side_effect=InternalException("Server not valid"),
        ):
            with patch.object(self.server, "extract_server", return_value=self.server):
                got = self.app.put("set_server_details", json=self.expected_dict_server)
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(self.failed_dict, retrieved_json)

    def test_setServer_response(self):
        with patch.object(FrontendAPI.hardware_controller.__class__, "setServer"):
            with patch.object(self.server, "extract_server", return_value=self.server):
                got = self.app.put("set_server_details", json=self.expected_dict_server)
                retrieved_json = json.loads(got.get_data())
                # get rid of python native data types
                self.assertEqual(retrieved_json, success_response)


if __name__ == "__main__":
    unittest.main()
