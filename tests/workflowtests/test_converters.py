from __future__ import annotations
import json
import unittest
from pathlib import Path
from typing import List
from unittest.mock import patch, Mock, mock_open
from matflow.exceptionpackage.MatFlowException import ConverterException
from matflow.frontendapi import keys, utilities
from matflow.workflow.frontend_version import FrontendVersion
from matflow.workflow.parameter_change import ParameterChange
from matflow.workflow.reduced_config_file import ReducedConfigFile
from matflow.workflow.template import Template


"""
Just like in API, keys etc. do not have to match real world use case due to mocking.
This is part of the integration test.
"""


class TemplateTest(unittest.TestCase):
    def setUp(self) -> None:
        # valid json, object irrelevant
        self.template_dict: dict = {keys.template_name: "scooby"}
        self.template: Template = Template("scooby", Path("/"))
        self.json_dumped = json.dumps(self.template_dict)
        self.dagMock = Mock()

    def test_extracting_valid(self):
        with patch.object(Template, "extract_dag_file", return_value=Path("/")):
            template: Template = Template.extract_template(self.json_dumped)
            self.assertEqual(template.get_name(), self.template.get_name())
            self.assertEqual(
                template.get_dag_definition_file(),
                self.template.get_dag_definition_file(),
            )

    def test_extracting_call_extract_dag(self):
        with patch.object(
            Template, "extract_dag_file", return_value=Path("/")
        ) as mock_method:
            Template.extract_template(self.json_dumped)
            assert mock_method.call_count > 0

    def test_extracting_dag_file_wrong(self):
        with patch.object(
            Template, "extract_dag_file", side_effect=ConverterException("whoops")
        ):
            with self.assertRaises(ConverterException):
                template: Template = Template.extract_template(self.json_dumped)

    def test_extracting_name_invalid(self):
        with self.assertRaises(ConverterException):
            template: Template = Template.extract_template(self.json_dumped)

    def test_dag_valid(self):
        json_dict: dict = {keys.dag_definition_name: "dag.py", keys.file_key: "bhbeb"}
        with patch.object(utilities, "decode_file", return_value=self.dagMock):
            with patch.object(utilities, "create_dir", return_value="/"):
                with patch.object(self.dagMock, "save"):
                    self.assertEqual(
                        Template.extract_dag_file(json_dict), Path("/dag.py")
                    )

    def test_dag_invalid_file_key_missing(self):
        json_dict: dict = {keys.dag_definition_name: "dag.py"}
        with self.assertRaises(ConverterException):
            with patch.object(utilities, "decode_file", return_value=self.dagMock):
                with patch.object(utilities, "create_dir", return_value="/"):
                    with patch.object(self.dagMock, "save"):
                        Template.extract_dag_file(json_dict)

    def test_dag_invalid_file_name_key_missing(self):
        json_dict: dict = {keys.file_key: "bhbeb"}
        with self.assertRaises(ConverterException):
            with patch.object(utilities, "decode_file", return_value=self.dagMock):
                with patch.object(utilities, "create_dir", return_value="/"):
                    with patch.object(self.dagMock, "save"):
                        Template.extract_dag_file(json_dict)

    def test_dag_call_decode(self):
        json_dict: dict = {keys.dag_definition_name: "dag.py", keys.file_key: "bhbeb"}
        with patch.object(
            utilities, "decode_file", return_value=self.dagMock
        ) as mock_method:
            with patch.object(utilities, "create_dir", return_value="/"):
                with patch.object(self.dagMock, "save"):
                    Template.extract_dag_file(json_dict)
                    assert mock_method.call_count > 0

    def test_dag_call_create_dir(self):
        json_dict: dict = {keys.dag_definition_name: "dag.py", keys.file_key: "bhbeb"}
        with patch.object(utilities, "decode_file", return_value=self.dagMock):
            with patch.object(utilities, "create_dir", return_value="/") as mock_method:
                with patch.object(self.dagMock, "save"):
                    Template.extract_dag_file(json_dict)
                    assert mock_method.call_count > 0

    @unittest.skip("No writing done in Template class")
    def test_dag_call_save(self):
        json_dict: dict = {keys.dag_definition_name: "dag.py", keys.file_key: "bhbeb"}
        with patch.object(utilities, "decode_file", return_value=self.dagMock):
            with patch.object(utilities, "create_dir", return_value="/"):
                with patch.object(self.dagMock, "save") as mock_method:
                    Template.extract_dag_file(json_dict)
                    assert mock_method.call_count > 0

    def test_encode_call_get_name(self):
        with patch.object(self.template, "get_name", return_value="zd") as mock_method:
            with patch.object(
                self.template, "get_dag_definition_file", return_value=self.dagMock
            ):
                with patch.object(utilities, "encode_file", return_value="zcezbe"):
                    self.template.encode_template()
                    assert mock_method.call_count > 0

    def test_encode_call_dag(self):
        with patch.object(Template, "get_name", return_value="zd"):
            with patch.object(
                Template, "get_dag_definition_file", return_value=self.dagMock
            ) as mock_method:
                with patch.object(utilities, "encode_file", return_value="zcezbe"):
                    self.template.encode_template()
                    assert mock_method.call_count > 0

    def test_encode_call_encode(self):
        with patch.object(Template, "get_name", return_value="zd"):
            with patch.object(
                Template, "get_dag_definition_file", return_value=self.dagMock
            ):
                with patch.object(
                    utilities, "encode_file", return_value="zcezbe"
                ) as mock_method:
                    self.template.encode_template()
                    assert mock_method.call_count > 0

    # encoding never raises exception -> always valid
    def test_encode(self):
        expected = {keys.file_key: "zcezbe", keys.template_name: "scooby"}
        with patch.object(Template, "get_name", return_value="scooby"):
            with patch.object(
                Template, "get_dag_definition_file", return_value=self.dagMock
            ):
                with patch.object(utilities, "encode_file", return_value="zcezbe"):
                    encoded = self.template.encode_template()
                    self.assertEqual(encoded, expected)


class ReducedConfigTest(unittest.TestCase):
    def setUp(self) -> None:
        self.reduced_config: ReducedConfigFile = ReducedConfigFile(
            "scooby", json.loads(json.dumps([("3", "4")]))
        )
        self.json_dumped = json.dumps(
            {keys.config_file_name: "scooby", keys.key_value_pairs_name: [("3", "4")]}
        )
        self.multipleConfigsKeyPairs = json.dumps(
            {
                keys.config_files: [
                    {
                        keys.config_file_name: "scooby",
                        keys.key_value_pairs_name: [("3", "4")],
                    }
                ]
            }
        )
        self.files_dumped = json.dumps(
            {
                keys.config_files: [
                    {keys.config_file_name: "scooby", keys.file_key: "doo"}
                ]
            }
        )

    def test_encode_call_get_file(self):
        with patch.object(
            ReducedConfigFile, "get_file_name", return_value="scooby"
        ) as mock_method:
            with patch.object(
                ReducedConfigFile, "get_key_value_pairs", return_value="doo"
            ):
                self.reduced_config.encode_config()
                assert mock_method.call_count > 0

    def test_encode_call_get_key_values(self):
        with patch.object(ReducedConfigFile, "get_file_name", return_value="scooby"):
            with patch.object(
                ReducedConfigFile, "get_key_value_pairs", return_value="doo"
            ) as mock_method:
                self.reduced_config.encode_config()
                assert mock_method.call_count > 0

    # encode always valid
    def test_encode_valid(self):
        expected = {keys.config_file_name: "scooby", keys.key_value_pairs_name: "doo"}
        with patch.object(ReducedConfigFile, "get_file_name", return_value="scooby"):
            with patch.object(
                ReducedConfigFile, "get_key_value_pairs", return_value="doo"
            ) as mock_method:
                encoded = self.reduced_config.encode_config()
                self.assertEqual(encoded, expected)

    def test_extract_config_valid(self):
        config = ReducedConfigFile.extract_config(self.json_dumped)
        self.assertEqual(config.get_file_name(), self.reduced_config.get_file_name())
        self.assertEqual(
            config.get_key_value_pairs(), self.reduced_config.get_key_value_pairs()
        )

    def test_extract_config_invalid_name(self):
        with self.assertRaises(ConverterException):
            ReducedConfigFile.extract_config(
                json.dumps({keys.key_value_pairs_name: [("3", "4")]})
            )

    def test_extract_config_invalid_pairs(self):
        with self.assertRaises(ConverterException):
            ReducedConfigFile.extract_config(json.dumps({keys.config_file_name: "je"}))

    def test_extract_configs_invalid_pairs(self):
        dumped = json.dumps({keys.config_files: [{keys.config_file_name: "scooby"}]})
        with self.assertRaises(ConverterException):
            ReducedConfigFile.extract_multiple_configs(dumped)

    def test_extract_configs_invalid_name(self):
        dumped = json.dumps(
            {keys.config_files: [{keys.key_value_pairs_name: [("3", "4")]}]}
        )
        with self.assertRaises(ConverterException):
            ReducedConfigFile.extract_multiple_configs(dumped)

    def test_extract_configs_invalid_main_key(self):
        dumped = json.dumps({keys.dag_definition_name: "Pluto"})
        with self.assertRaises(ConverterException):
            ReducedConfigFile.extract_multiple_configs(dumped)

    def test_extract_configs_valid(self):
        configs: List[ReducedConfigFile] = ReducedConfigFile.extract_multiple_configs(
            self.multipleConfigsKeyPairs
        )
        # only 1 object
        self.assertEqual(len(configs), 1)
        self.assertEqual(
            configs[0].get_file_name(), self.reduced_config.get_file_name()
        )
        self.assertEqual(
            configs[0].get_key_value_pairs(), self.reduced_config.get_key_value_pairs()
        )

    @unittest.skip("no write action")
    def test_extract_config_files_call_write(self):
        with patch.object(utilities, "create_dir", return_value="/"):
            with patch.object(utilities, "decode_file", return_value="encoded_file"):
                with patch("builtins.open", mock_open(read_data="data")) as mock_file:
                    ReducedConfigFile.extract_multiple_config_files(self.files_dumped)
                    mock_file.assert_called_with("/scooby", "wb")

    def test_extract_config_files_call_create_dir(self):
        with patch.object(utilities, "create_dir", return_value="/") as mock_method:
            with patch.object(utilities, "decode_file", return_value="encoded_file"):
                with patch("builtins.open", mock_open(read_data="data")):
                    ReducedConfigFile.extract_multiple_config_files(self.files_dumped)
                    assert mock_method.call_count > 0

    def test_extract_config_files_call_decode_file(self):
        with patch.object(utilities, "create_dir", return_value="/"):
            with patch.object(
                utilities, "decode_file", return_value="encoded_file"
            ) as mock_method:
                with patch("builtins.open", mock_open(read_data="data")):
                    ReducedConfigFile.extract_multiple_config_files(self.files_dumped)
                    assert mock_method.call_count > 0

    def test_extract_config_files_valid(self):
        with patch.object(utilities, "create_dir", return_value="/"):
            with patch.object(utilities, "decode_file", return_value="encoded_file"):
                with patch("builtins.open", mock_open(read_data="data")):
                    path: Path = ReducedConfigFile.extract_multiple_config_files(
                        self.files_dumped
                    )
                    self.assertEqual(path, Path("/"))

    def test_extract_config_files_invalid_main_key(self):
        to_dump = json.dumps({})
        with self.assertRaises(ConverterException):
            with patch.object(utilities, "create_dir", return_value="/"):
                with patch.object(
                    utilities, "decode_file", return_value="encoded_file"
                ):
                    with patch("builtins.open", mock_open(read_data="data")):
                        path: Path = ReducedConfigFile.extract_multiple_config_files(
                            to_dump
                        )
                        self.assertEqual(path, Path("/"))

    def test_extract_config_files_invalid_file_key(self):
        to_dump = json.dumps({keys.config_files: [{keys.config_file_name: "scooby"}]})
        with self.assertRaises(ConverterException):
            with patch.object(utilities, "create_dir", return_value="/"):
                with patch.object(
                    utilities, "decode_file", return_value="encoded_file"
                ):
                    with patch("builtins.open", mock_open(read_data="data")):
                        path: Path = ReducedConfigFile.extract_multiple_config_files(
                            to_dump
                        )
                        self.assertEqual(path, Path("/"))

    def test_extract_config_files_invalid_file_name_key(self):
        to_dump = json.dumps({keys.config_files: [{keys.file_key: "doo"}]})
        with self.assertRaises(ConverterException):
            with patch.object(utilities, "create_dir", return_value="/"):
                with patch.object(
                    utilities, "decode_file", return_value="encoded_file"
                ):
                    with patch("builtins.open", mock_open(read_data="data")):
                        path: Path = ReducedConfigFile.extract_multiple_config_files(
                            to_dump
                        )
                        self.assertEqual(path, Path("/"))


class FrontendVersionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.change = Mock()
        self.version_number = Mock()
        self.frontend_version = FrontendVersion(
            self.version_number, "scooby", [self.change]
        )

    # can only be valid
    def test_encode_version_valid(self):
        expected = {
            keys.version_note_name: "scooby",
            keys.frontend_versions_changes: ["boo"],
            keys.version_number_name: 1,
        }
        with patch.object(self.version_number, "get_number", return_value=1):
            with patch.object(self.change, "encode", return_value="boo"):
                encoded = self.frontend_version.encode_version()
                self.assertEqual(encoded, expected)

    def test_encode_call_get_number(self):
        with patch.object(
            self.version_number, "get_number", return_value=1
        ) as mock_method:
            with patch.object(self.change, "encode", return_value="boo"):
                encoded = self.frontend_version.encode_version()
                assert mock_method.call_count > 0

    def test_encode_call_encode(self):
        with patch.object(self.version_number, "get_number", return_value=1):
            with patch.object(self.change, "encode", return_value="boo") as mock_method:
                encoded = self.frontend_version.encode_version()
                assert mock_method.call_count > 0


class ParameterChangeTest(unittest.TestCase):
    # encoding can only be valid
    def test_encoding_valid(self):
        change: ParameterChange = ParameterChange(
            "scooby", "dooby", "doo", "hoo", "Pluto"
        )
        expected = {
            keys.config_file_name: "Pluto",
            keys.old_key: "scooby",
            keys.new_key: "dooby",
            keys.old_value: "doo",
            keys.new_value: "hoo",
        }
        self.assertEqual(expected, change.encode())


if __name__ == "__main__":
    unittest.main()
