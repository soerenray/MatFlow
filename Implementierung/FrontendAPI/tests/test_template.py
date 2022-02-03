import json
import unittest
from unittest.mock import patch, Mock
from Implementierung.FrontendAPI.api import app, FrontendAPI
from Implementierung.FrontendAPI import keys, utilities
from Implementierung.ExceptionPackage.MatFlowException import InternalException
from Implementierung.workflow.template import Template
from copy import deepcopy

success_response: dict = {"statusCode": 607}


class TemplateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()
        self.failed_dict = {keys.status_code_name: InternalException("scooby not found").get_status_code()}
        self.templateMock = Mock()
        self.imageMock = Mock()

    def test_create_template_call_extract_template(self):
        with patch.object(Template, "extract_template", return_value=self.templateMock) as mock_method:
            with patch.object(FrontendAPI.workflow_manager.__class__, "create_template"):
                self.app.post('create_template', json=json.dumps({"bla": "bla"}))
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method.call_count > 0

    def test_create_template_call_wf_manager(self):
        with patch.object(Template, "extract_template", return_value=self.templateMock):
            with patch.object(FrontendAPI.workflow_manager.__class__, "create_template") as mock_method:
                self.app.post('create_template', json=json.dumps({"bla": "bla"}))
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method.call_count > 0

    def test_create_template_response_fail(self):
        with patch.object(Template, "extract_template", side_effect=InternalException("boo")):
            with patch.object(FrontendAPI.workflow_manager.__class__, "create_template"):
                got = self.app.post('create_template', json=json.dumps({"bla": "bla"}))
                retrieved_json = json.loads(got.get_data())
                self.assertEqual(retrieved_json, self.failed_dict)

    def test_create_template_response_valid(self):
        with patch.object(Template, "extract_template", return_value=self.templateMock):
            with patch.object(FrontendAPI.workflow_manager.__class__, "create_template"):
                got = self.app.post('create_template', json=json.dumps({"bla": "bla"}))
                retrieved_json = json.loads(got.get_data())
                self.assertEqual(retrieved_json, success_response)

    def test_get_all_template_names_call_wf_manager(self):
        with patch.object(FrontendAPI.workflow_manager.__class__, "get_template_names", return_value={"ha": "he"}) \
                as mock_method:
            self.app.get('get_all_template_names')
            # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
            assert mock_method.call_count > 0

    def test_get_all_template_names_response(self):
        # no fail possible
        with patch.object(FrontendAPI.workflow_manager.__class__, "get_template_names",
                          return_value=["te1", "te2"]):
            got = self.app.get('get_all_template_names')
            retrieved_json: dict = json.loads(got.get_data())
            expected_dict: dict = {keys.template_names: ["te1", "te2"]}
            expected_dict.update(success_response)
            expected_dict = json.loads(json.dumps(expected_dict))
            self.assertEqual(retrieved_json, expected_dict)

    def test_get_template_call_wf_manager(self):
        with patch.object(FrontendAPI.workflow_manager.__class__, "get_template_from_name",
                          return_value=self.templateMock) as mock_method:
            with patch.object(self.templateMock, "encode_template",
                              return_value={"he": "ha"}):
                self.app.get('get_template', json=json.dumps({keys.template_name: "hu"}))
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method.call_count > 0

    def test_get_template_call_encode(self):
        with patch.object(FrontendAPI.workflow_manager.__class__, "get_template_from_name",
                          return_value=self.templateMock):
            with patch.object(self.templateMock, "encode_template",
                              return_value={"he": "ha"}) as mock_method:
                self.app.get('get_template', json=json.dumps({keys.template_name: "hu"}))
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method.call_count > 0

    def test_get_template_response_fail(self):
        with patch.object(FrontendAPI.workflow_manager.__class__, "get_template_from_name",
                          side_effect=InternalException("boo")):
            with patch.object(Template, "encode_template",
                              return_value={"he": "ha"}):
                got = self.app.get('get_template', json=json.dumps({keys.template_name: "hu"}))
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(retrieved_json, self.failed_dict)

    def test_get_template_response_valid(self):
        with patch.object(FrontendAPI.workflow_manager.__class__, "get_template_from_name",
                          return_value=self.templateMock):
            with patch.object(self.templateMock, "encode_template",
                              return_value={"he": "ha"}):
                got = self.app.get('get_template', json=json.dumps({keys.template_name: "hu"}))
                retrieved_json: dict = json.loads(got.get_data())
                expected_dict: dict = deepcopy(success_response)
                expected_dict.update({"he": "ha"})
                expected_dict = json.loads(json.dumps(expected_dict))
                self.assertEqual(retrieved_json, expected_dict)

    def test_get_graph_call_extract(self):
        with patch.object(Template, "extract_template", return_value=self.templateMock) as mock_method:
            with patch.object(FrontendAPI.workflow_manager.__class__, "create_template"):
                with patch.object(FrontendAPI.workflow_manager.__class__, "get_dag_representation_from_template",
                                  return_value=self.imageMock):
                    with patch.object(utilities, "encode_file", return_value= {"bla": "ble"}):
                        self.app.get('get_graph_for_temporary_template', json=json.dumps({"hu": "bla"}))
                        # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called()
                        # throws error
                        assert mock_method.call_count > 0

    def test_get_graph_call_create_template(self):
        with patch.object(Template, "extract_template", return_value=self.templateMock):
            with patch.object(FrontendAPI.workflow_manager.__class__, "create_template") as mock_method:
                with patch.object(FrontendAPI.workflow_manager.__class__, "get_dag_representation_from_template",
                                  return_value=self.imageMock):
                    with patch.object(utilities, "encode_file", return_value= {"bla": "ble"}):
                        self.app.get('get_graph_for_temporary_template', json=json.dumps({"hu": "bla"}))
                        # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called()
                        # throws error
                        assert mock_method.call_count > 0

    def test_get_graph_call_get_dag(self):
        with patch.object(Template, "extract_template", return_value=self.templateMock):
            with patch.object(FrontendAPI.workflow_manager.__class__, "create_template"):
                with patch.object(FrontendAPI.workflow_manager.__class__, "get_dag_representation_from_template",
                                  return_value=self.imageMock) as mock_method:
                    with patch.object(utilities, "encode_file", return_value= {"bla": "ble"}):
                        self.app.get('get_graph_for_temporary_template', json=json.dumps({"hu": "bla"}))
                        # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called()
                        # throws error
                        assert mock_method.call_count > 0

    def test_get_graph_call_encode_file(self):
        with patch.object(Template, "extract_template", return_value=self.templateMock):
            with patch.object(FrontendAPI.workflow_manager.__class__, "create_template"):
                with patch.object(FrontendAPI.workflow_manager.__class__, "get_dag_representation_from_template",
                                  return_value=self.imageMock):
                    with patch.object(utilities, "encode_file", return_value= {"bla": "ble"}) as mock_method:
                        self.app.get('get_graph_for_temporary_template', json=json.dumps({"hu": "bla"}))
                        # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called()
                        # throws error
                        assert mock_method.call_count > 0

    def test_get_graph_response_fail(self):
        with patch.object(Template, "extract_template", side_effect=InternalException("boo")):
            with patch.object(FrontendAPI.workflow_manager.__class__, "create_template"):
                with patch.object(FrontendAPI.workflow_manager.__class__, "get_dag_representation_from_template",
                                  return_value=self.imageMock) as mock_method:
                    with patch.object(utilities, "encode_file", return_value= {"bla": "ble"}):
                        got = self.app.get('get_graph_for_temporary_template', json=json.dumps({"hu": "bla"}))
                        retrieved_data: dict = json.loads(got.get_data())
                        self.assertEqual(retrieved_data, self.failed_dict)

    def test_get_graph_response_valid(self):
        with patch.object(Template, "extract_template", return_value=self.templateMock):
            with patch.object(FrontendAPI.workflow_manager.__class__, "create_template"):
                with patch.object(FrontendAPI.workflow_manager.__class__, "get_dag_representation_from_template",
                                  return_value=self.imageMock):
                    with patch.object(utilities, "encode_file", return_value={"bla": "ble"}):
                        got = self.app.get('get_graph_for_temporary_template', json=json.dumps({"hu": "bla"}))
                        retrieved_json: dict = json.loads(got.get_data())
                        expected_dict: dict = deepcopy(success_response)
                        expected_dict.update({"bla": "ble"})
                        expected_dict = json.loads(json.dumps(expected_dict))
                        self.assertEqual(expected_dict, retrieved_json)


if __name__ == '__main__':
    unittest.main()
