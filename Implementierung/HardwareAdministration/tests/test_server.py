import json
import unittest
from unittest.mock import Mock, patch
from Implementierung.ExceptionPackage.MatFlowException import ConverterException, InternalException
from Implementierung.FrontendAPI import keys
from Implementierung.FrontendAPI.api import app
from Implementierung.HardwareAdministration.Server import Server


class ServerTest(unittest.TestCase):
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
        self.expected_dict_server_2: dict = {
            keys.server_name: "server",
            keys.server_status_name: "online",
            keys.server_address_name: "127.0.0.1",
            keys.container_limit_name: 4,
            keys.server_resources_name: ("ha", "ha"),
            keys.selected_for_execution_name: True,
        }
        self.server = Mock()
        self.failed_dict = {
            keys.status_code_name: InternalException(
                "Server not found"
            ).get_status_code()
        }
    # only valid response
    def test_server_encoding(self):
        server: Server = Server()
        expected = {'serverName': 'server', 'serverAddress': '192.168.0.81', 'serverStatus': True,
                    'containerLimit': 20, 'selectedForExecution': True, 'serverResources': [1,2]}
        with patch.object(Server, "getRessources", return_value=[1,2]):
            encoding = server.encode_server()
            self.assertEqual(encoding, expected)

    def test_server_encoding_call_name(self):
        with patch.object(Server, "getName", return_value="scooby") as mock_method:
            with patch.object(Server, "getAddress", return_value="local"):
                with patch.object(Server, "getStatus", return_value="online"):
                    with patch.object(Server, "getContainerLimit", return_value=20):
                        with patch.object(Server, "isSelectedForExecution", return_value=True):
                            with patch.object(Server, "getRessources", return_value=(1,2)):
                                server: Server = Server()
                                server.encode_server()
                                assert mock_method.call_count > 0

    def test_server_encoding_call_address(self):
        with patch.object(Server, "getName", return_value="scooby"):
            with patch.object(Server, "getAddress", return_value="local") as mock_method:
                with patch.object(Server, "getStatus", return_value="online"):
                    with patch.object(Server, "getContainerLimit", return_value=20):
                        with patch.object(Server, "isSelectedForExecution", return_value=True):
                            with patch.object(Server, "getRessources", return_value=(1, 2)):
                                server: Server = Server()
                                server.encode_server()
                                assert mock_method.call_count > 0

    def test_server_encoding_call_status(self):
        with patch.object(Server, "getName", return_value="scooby"):
            with patch.object(Server, "getAddress", return_value="local"):
                with patch.object(Server, "getStatus", return_value="online") as mock_method:
                    with patch.object(Server, "getContainerLimit", return_value=20):
                        with patch.object(Server, "isSelectedForExecution", return_value=True):
                            with patch.object(Server, "getRessources", return_value=(1, 2)):
                                server: Server = Server()
                                server.encode_server()
                                assert mock_method.call_count > 0

    def test_server_encoding_call_container_limit(self):
        with patch.object(Server, "getName", return_value="scooby"):
            with patch.object(Server, "getAddress", return_value="local"):
                with patch.object(Server, "getStatus", return_value="online"):
                    with patch.object(Server, "getContainerLimit", return_value=20) as mock_method:
                        with patch.object(Server, "isSelectedForExecution", return_value=True):
                            with patch.object(Server, "getRessources", return_value=(1, 2)):
                                server: Server = Server()
                                server.encode_server()
                                assert mock_method.call_count > 0

    def test_server_encoding_call_selected(self):
        with patch.object(Server, "getName", return_value="scooby"):
            with patch.object(Server, "getAddress", return_value="local"):
                with patch.object(Server, "getStatus", return_value="online"):
                    with patch.object(Server, "getContainerLimit", return_value=20):
                        with patch.object(Server, "isSelectedForExecution", return_value=True) as mock_method:
                            with patch.object(Server, "getRessources", return_value=(1, 2)):
                                server: Server = Server()
                                server.encode_server()
                                assert mock_method.call_count > 0

    def test_server_encoding_call_resources(self):
        with patch.object(Server, "getName", return_value="scooby"):
            with patch.object(Server, "getAddress", return_value="local"):
                with patch.object(Server, "getStatus", return_value="online"):
                    with patch.object(Server, "getContainerLimit", return_value=20):
                        with patch.object(Server, "isSelectedForExecution", return_value=True):
                            with patch.object(Server, "getRessources", return_value=(1, 2)) as mock_method:
                                server: Server = Server()
                                server.encode_server()
                                assert mock_method.call_count > 0

    def test_extraction_valid(self):
        # self.expected_dict_server_2 has resources as tuple, not list
        extracted = Server.extract_server(json.dumps(self.expected_dict_server_2))
        self.assertEqual(extracted.getName(), self.expected_dict_server[keys.server_name])
        self.assertEqual(extracted.getStatus(), self.expected_dict_server[keys.server_status_name])
        # server resources should be tuple -> first element in list
        self.assertEqual(extracted.getRessources(), self.expected_dict_server_2[keys.server_resources_name])
        self.assertEqual(extracted.getAddress(), self.expected_dict_server[keys.server_address_name])
        self.assertEqual(extracted.getContainerLimit(), self.expected_dict_server[keys.container_limit_name])
        self.assertEqual(extracted.isSelectedForExecution(),
                         self.expected_dict_server[keys.selected_for_execution_name])

    def test_extraction_invalid_name(self):
        to_dump = {
            keys.server_status_name: "online",
            keys.server_address_name: "127.0.0.1",
            keys.container_limit_name: 4,
            keys.server_resources_name: ("ha", "ha"),
            keys.selected_for_execution_name: True,
        }
        with self.assertRaises(ConverterException):
            Server.extract_server(json.dumps(to_dump))

    def test_extraction_invalid_status(self):
        to_dump = {
            keys.server_name: "server",
            keys.server_address_name: "127.0.0.1",
            keys.container_limit_name: 4,
            keys.server_resources_name: ("ha", "ha"),
            keys.selected_for_execution_name: True,
        }
        with self.assertRaises(ConverterException):
            Server.extract_server(json.dumps(to_dump))

    def test_extraction_invalid_address(self):
        to_dump = {
            keys.server_name: "server",
            keys.server_status_name: "online",
            keys.container_limit_name: 4,
            keys.server_resources_name: ("ha", "ha"),
            keys.selected_for_execution_name: True,
        }
        with self.assertRaises(ConverterException):
            Server.extract_server(json.dumps(to_dump))

    def test_extraction_invalid_limit(self):
        to_dump = {
            keys.server_name: "server",
            keys.server_address_name: "127.0.0.1",
            keys.server_status_name: "online",
            keys.server_resources_name: ("ha", "ha"),
            keys.selected_for_execution_name: True,
        }
        with self.assertRaises(ConverterException):
            Server.extract_server(json.dumps(to_dump))

    def test_extraction_invalid_resource(self):
        to_dump = {
            keys.server_name: "server",
            keys.server_address_name: "127.0.0.1",
            keys.server_status_name: "online",
            keys.container_limit_name: 4,
            keys.selected_for_execution_name: True,
        }
        with self.assertRaises(ConverterException):
            Server.extract_server(json.dumps(to_dump))

    def test_extraction_invalid_execution(self):
        to_dump = {
            keys.server_name: "server",
            keys.server_address_name: "127.0.0.1",
            keys.server_status_name: "online",
            keys.container_limit_name: 4,
            keys.server_resources_name: ("ha", "ha"),
        }
        with self.assertRaises(ConverterException):
            Server.extract_server(json.dumps(to_dump))


if __name__ == '__main__':
    unittest.main()
