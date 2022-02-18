import unittest
import json
from pathlib import Path
from unittest.mock import patch, Mock
from matflow.workflow.reduced_config_file import ReducedConfigFile
from matflow.exceptionpackage.MatFlowException import InternalException
from matflow.frontendapi import keys
from matflow.frontendapi.api import app, FrontendAPI


success_response: dict = {"statusCode": 607}


class WorkflowInstanceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.frontendVersion1 = Mock()
        self.return_version_dict = {"he": "Scooby"}
        self.frontendVersion2 = Mock()
        self.app = app.test_client()
        self.failed_dict = {
            keys.status_code_name: InternalException("whoops").get_status_code()
        }
        self.mockConfig = Mock()

    def test_get_wf_instance_versions_call_wf_manager(self):
        with patch.object(
            FrontendAPI.workflow_manager.__class__,
            "get_versions_from_workflow_instance",
            return_value=[self.frontendVersion1, self.frontendVersion2],
        ) as mock_method:
            with patch.object(
                self.frontendVersion1, "encode_version", return_value=dict()
            ):
                with patch.object(
                    self.frontendVersion2, "encode_version", return_value=dict()
                ):
                    self.app.get(
                        "get_wf_instance_versions",
                        json=json.dumps({keys.workflow_instance_name: "bla"}),
                    )
                    # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called()
                    # throws error
                    assert mock_method.call_count > 0

    def test_get_wf_instance_versions_call_encode_1(self):
        with patch.object(
            FrontendAPI.workflow_manager.__class__,
            "get_versions_from_workflow_instance",
            return_value=[self.frontendVersion1, self.frontendVersion2],
        ):
            with patch.object(
                self.frontendVersion1, "encode_version", return_value=dict()
            ) as mock_method_2:
                with patch.object(
                    self.frontendVersion2, "encode_version", return_value=dict()
                ):
                    self.app.get(
                        "get_wf_instance_versions",
                        json=json.dumps({keys.workflow_instance_name: "bla"}),
                    )
                    # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called()
                    # throws error
                    assert mock_method_2.call_count > 0

    def test_get_wf_instance_versions_call_encode_2(self):
        with patch.object(
            FrontendAPI.workflow_manager.__class__,
            "get_versions_from_workflow_instance",
            return_value=[self.frontendVersion1, self.frontendVersion2],
        ):
            with patch.object(
                self.frontendVersion1, "encode_version", return_value=dict()
            ):
                with patch.object(
                    self.frontendVersion2, "encode_version", return_value=dict()
                ) as mock_method_3:
                    self.app.get(
                        "get_wf_instance_versions",
                        json=json.dumps({keys.workflow_instance_name: "bla"}),
                    )
                    # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called()
                    # throws error
                    assert mock_method_3.call_count > 0

    def test_get_wf_instance_versions_response_fail(self):
        with patch.object(
            FrontendAPI.workflow_manager.__class__,
            "get_versions_from_workflow_instance",
            side_effect=InternalException("whoops"),
        ):
            with patch.object(
                self.frontendVersion1, "encode_version", return_value=dict()
            ):
                with patch.object(
                    self.frontendVersion2, "encode_version", return_value=dict()
                ):
                    got = self.app.get(
                        "get_wf_instance_versions",
                        json=json.dumps({keys.workflow_instance_name: "bla"}),
                    )
                    retrieved_json: dict = json.loads(got.get_data())
                    self.assertEqual(retrieved_json, self.failed_dict)

    def test_get_wf_instance_versions_response_valid(self):
        with patch.object(
            self.frontendVersion1, "encode_version", return_value={"ha": "he"}
        ):
            with patch.object(
                FrontendAPI.workflow_manager.__class__,
                "get_versions_from_workflow_instance",
                return_value=[self.frontendVersion1, self.frontendVersion1],
            ):
                got = self.app.get(
                    "get_wf_instance_versions",
                    json=json.dumps({keys.workflow_instance_name: "bla"}),
                )
                retrieved_json: dict = json.loads(got.get_data())
                expected_dict: dict = json.loads(
                    json.dumps(
                        {
                            keys.versions_name: [
                                self.frontendVersion1.encode_version(),
                                self.frontendVersion1.encode_version(),
                            ]
                        }
                    )
                )
                expected_dict.update(success_response)
                self.assertEqual(retrieved_json, expected_dict)

    def test_replace_wf_instance_active_versions_call_wf_manager(self):
        with patch.object(
            FrontendAPI.workflow_manager.__class__, "set_active_version_through_number"
        ) as mock_method:
            self.app.put(
                "replace_wf_instance_active_version",
                json=json.dumps(
                    {
                        keys.workflow_instance_name: "bla",
                        keys.version_number_name: "scooby",
                    }
                ),
            )
            # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
            assert mock_method.call_count > 0

    def test_replace_wf_instance_active_versions_fail(self):
        with patch.object(
            FrontendAPI.workflow_manager.__class__,
            "set_active_version_through_number",
            side_effect=InternalException("oops"),
        ):
            got = self.app.put(
                "replace_wf_instance_active_version",
                json=json.dumps(
                    {
                        keys.workflow_instance_name: "bla",
                        keys.version_number_name: "scooby",
                    }
                ),
            )
            retrieved_json: dict = json.loads(got.get_data())
            self.assertEqual(retrieved_json, self.failed_dict)

    def test_replace_wf_instance_active_versions_valid(self):
        with patch.object(
            FrontendAPI.workflow_manager.__class__, "set_active_version_through_number"
        ):
            got = self.app.put(
                "replace_wf_instance_active_version",
                json=json.dumps(
                    {
                        keys.workflow_instance_name: "bla",
                        keys.version_number_name: "scooby",
                    }
                ),
            )
            retrieved_json: dict = json.loads(got.get_data())
            self.assertEqual(retrieved_json, success_response)

    def test_create_version_of_wf_instance_call_extract_files(self):
        with patch.object(
            FrontendAPI.workflow_manager.__class__,
            "create_new_version_of_workflow_instance",
        ) as mock_method:
            with patch.object(
                ReducedConfigFile, "extract_multiple_configs", return_value=[]
            ):
                self.app.post(
                    "create_version_of_wf_instance",
                    json=json.dumps(
                        {
                            keys.workflow_instance_name: "bla",
                            keys.version_note_name: "scooby",
                            keys.config_files: [],
                        }
                    ),
                )
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method.call_count > 0

    def test_create_version_of_wf_instance_call_wf_manager(self):
        with patch.object(
            FrontendAPI.workflow_manager.__class__,
            "create_new_version_of_workflow_instance",
        ):
            with patch.object(
                ReducedConfigFile, "extract_multiple_configs", return_value=[]
            ) as mock_method_2:
                self.app.post(
                    "create_version_of_wf_instance",
                    json=json.dumps(
                        {
                            keys.workflow_instance_name: "bla",
                            keys.version_note_name: "scooby",
                            keys.config_files: [],
                        }
                    ),
                )
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method_2.call_count > 0

    def test_create_version_of_wf_instance_response_fail(self):
        with patch.object(
            FrontendAPI.workflow_manager.__class__,
            "create_new_version_of_workflow_instance",
            side_effect=InternalException("oops"),
        ):
            with patch.object(
                ReducedConfigFile, "extract_multiple_configs", return_value=[]
            ):
                got = self.app.post(
                    "create_version_of_wf_instance",
                    json=json.dumps(
                        {
                            keys.workflow_instance_name: "bla",
                            keys.version_note_name: "scooby",
                            keys.config_files: [],
                        }
                    ),
                )
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(retrieved_json, self.failed_dict)

    def test_create_version_of_wf_instance_response_valid(self):
        with patch.object(
            FrontendAPI.workflow_manager.__class__,
            "create_new_version_of_workflow_instance",
        ):
            with patch.object(
                ReducedConfigFile, "extract_multiple_configs", return_value=[]
            ):
                got = self.app.post(
                    "create_version_of_wf_instance",
                    json=json.dumps(
                        {
                            keys.workflow_instance_name: "bla",
                            keys.version_note_name: "scooby",
                            keys.config_files: [],
                        }
                    ),
                )
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(retrieved_json, success_response)

    def test_get_config_from_wf_instance_call_wf_manager(self):
        with patch.object(
            FrontendAPI.workflow_manager.__class__,
            "get_key_value_pairs_from_config_file",
            return_value=self.mockConfig,
        ) as mock_method:
            with patch.object(
                self.mockConfig, "encode_config", return_value={"he": "du"}
            ):
                self.app.get(
                    "get_config_from_wf_instance",
                    json=json.dumps(
                        {
                            keys.workflow_instance_name: "bla",
                            keys.config_file_name: "scooby",
                        }
                    ),
                )
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method.call_count > 0

    def test_get_config_from_wf_instance_call_encode(self):
        with patch.object(
            FrontendAPI.workflow_manager.__class__,
            "get_key_value_pairs_from_config_file",
            return_value=self.mockConfig,
        ):
            with patch.object(
                self.mockConfig, "encode_config", return_value={"he": "du"}
            ) as mock_method:
                self.app.get(
                    "get_config_from_wf_instance",
                    json=json.dumps(
                        {
                            keys.workflow_instance_name: "bla",
                            keys.config_file_name: "scooby",
                        }
                    ),
                )
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method.call_count > 0

    def test_get_config_from_wf_instance_response_fail(self):
        with patch.object(
            FrontendAPI.workflow_manager.__class__,
            "get_key_value_pairs_from_config_file",
            side_effect=InternalException("whoops"),
        ):
            with patch.object(
                self.mockConfig, "encode_config", return_value={"he": "du"}
            ):
                got = self.app.get(
                    "get_config_from_wf_instance",
                    json=json.dumps(
                        {
                            keys.workflow_instance_name: "bla",
                            keys.config_file_name: "scooby",
                        }
                    ),
                )
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(retrieved_json, self.failed_dict)

    def test_get_config_from_wf_instance_response_valid(self):
        with patch.object(
            FrontendAPI.workflow_manager.__class__,
            "get_key_value_pairs_from_config_file",
            return_value=self.mockConfig,
        ):
            with patch.object(
                self.mockConfig, "encode_config", return_value={"he": "du"}
            ):
                got = self.app.get(
                    "get_config_from_wf_instance",
                    json=json.dumps(
                        {
                            keys.workflow_instance_name: "bla",
                            keys.config_file_name: "scooby",
                        }
                    ),
                )
                retrieved_json: dict = json.loads(got.get_data())
                expected_dict: dict = {"he": "du"}
                expected_dict.update(success_response)
                # get rid of python native data types
                expected_dict = json.loads(json.dumps(expected_dict))
                self.assertEqual(retrieved_json, expected_dict)

    def test_create_wf_instance_call_extract_configs(self):
        with patch.object(
            ReducedConfigFile, "extract_multiple_config_files", return_value=Path("/")
        ) as mock_method:
            with patch.object(
                FrontendAPI.workflow_manager.__class__,
                "create_workflow_instance_from_template",
            ):
                self.app.post(
                    "create_workflow_instance",
                    json=json.dumps(
                        {keys.workflow_instance_name: "bla", keys.template_name: "blue"}
                    ),
                )
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method.call_count > 0

    def test_create_wf_instance_call_wf_manager(self):
        with patch.object(
            ReducedConfigFile, "extract_multiple_config_files", return_value=Path("/")
        ):
            with patch.object(
                FrontendAPI.workflow_manager.__class__,
                "create_workflow_instance_from_template",
            ) as mock_method:
                self.app.post(
                    "create_workflow_instance",
                    json=json.dumps(
                        {keys.workflow_instance_name: "bla", keys.template_name: "blue"}
                    ),
                )
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method.call_count > 0

    def test_create_wf_instance_response_fail(self):
        with patch.object(
            ReducedConfigFile,
            "extract_multiple_config_files",
            side_effect=InternalException("whoops"),
        ):
            with patch.object(
                FrontendAPI.workflow_manager.__class__,
                "create_workflow_instance_from_template",
            ):
                got = self.app.post(
                    "create_workflow_instance",
                    json=json.dumps(
                        {keys.workflow_instance_name: "bla", keys.template_name: "blue"}
                    ),
                )
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(retrieved_json, self.failed_dict)

    def test_create_wf_instance_response_valid(self):
        with patch.object(ReducedConfigFile, "extract_multiple_config_files"):
            with patch.object(
                FrontendAPI.workflow_manager.__class__,
                "create_workflow_instance_from_template",
            ):
                got = self.app.post(
                    "create_workflow_instance",
                    json=json.dumps(
                        {keys.workflow_instance_name: "bla", keys.template_name: "blue"}
                    ),
                )
                retrieved_json: dict = json.loads(got.get_data())
                self.assertEqual(retrieved_json, success_response)

    def test_get_all_wf_instances_names_and_config_file_names_call_wf_manager(self):
        with patch.object(self.mockConfig, "encode_config", return_value={"ha": "he"}):
            with patch.object(
                FrontendAPI.workflow_manager.__class__,
                "get_names_of_workflows_and_config_files",
                return_value={
                    "name1": [
                        self.mockConfig.encode_config(),
                        self.mockConfig.encode_config(),
                    ],
                    "name2": [],
                },
            ) as mock_method:
                self.app.get("get_all_wf_instances_names_and_config_file_names")
                # assert mock_method.assert_called() does not work whereas mock_method.assert_not_called() throws error
                assert mock_method.call_count > 0

    def test_get_all_wf_instances_names_and_config_file_names_response(self):
        with patch.object(self.mockConfig, "encode_config", return_value={"ha": "he"}):
            return_dict: dict = {
                "name1": [
                    self.mockConfig.encode_config(),
                    self.mockConfig.encode_config(),
                ],
                "name2": [],
            }
            with patch.object(
                FrontendAPI.workflow_manager.__class__,
                "get_names_of_workflows_and_config_files",
                return_value=return_dict,
            ):
                got = self.app.get("get_all_wf_instances_names_and_config_file_names")
                retrieved_json: dict = json.loads(got.get_data())
                expected_dict: dict = {keys.names_and_configs: return_dict}
                expected_dict.update(success_response)
                expected_dict = json.loads(json.dumps(expected_dict))
                self.assertEqual(expected_dict, retrieved_json)


if __name__ == "__main__":
    unittest.main()
