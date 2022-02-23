import unittest
from pathlib import Path
from typing import Dict, List
from unittest.mock import patch, Mock

from matflow.database.WorkflowData import WorkflowData
from matflow.workflow.database_version import DatabaseVersion
from matflow.workflow.version_number import VersionNumber
from matflow.workflow.workflow_instance import WorkflowInstance
from matflow.database.DatabaseTable import DatabaseTable
from matflow.exceptionpackage.MatFlowException import InternalException


class TestWorkflowDataSetup(unittest.TestCase):
    workflow_data: WorkflowData

    def setUp(self) -> None:
        self.workflow_data = WorkflowData.get_instance()


class TestWorkflowData(TestWorkflowDataSetup):
    def test_get_Instance(self):
        self.assertEqual(self.workflow_data, WorkflowData.get_instance())

    def test_create_wf_instance1(self):
        # when workflow already exists in db
        with patch.object(
            DatabaseTable,
            "check_for",
            return_value=True,
        ) as mock_check_for:  # is only called once to check if workflow with called name already exists
            # Arrange
            workflow = WorkflowInstance("workflow1", Path(".test"), Path("."))
            ex_path = Path(".")

            # Act/Assert
            with self.assertRaises(InternalException) as error:
                self.assertRaises(
                    InternalException,
                    self.workflow_data.create_wf_instance(workflow, ex_path),
                )

            # Assert
            mock_check_for.assert_called_once()
            self.assertIn("workflow1", str(mock_check_for.call_args_list))

    def test_create_wf_instance2(self):
        # basic test if all functions are called
        # Arrange
        workflow = WorkflowInstance("workflow1", Path(".test"), Path("."))
        ex_path = Path("./testfiles")

        with patch.object(
            DatabaseTable,
            "get_one",
            return_value=(42,),  # still return tuple
        ) as mock_get_one:
            with patch.object(
                DatabaseTable, "check_for", return_value=False
            ) as mock_check_for:
                with patch.object(
                    DatabaseTable,
                    "set",
                ) as mock_set:
                    # Act
                    self.workflow_data.create_wf_instance(workflow, ex_path)

                    # Assert
                    # (weak) called at least so many times as files from directory have to be passed
                    size = 0
                    for _ in ex_path.iterdir():
                        size += 1
                    self.assertTrue(mock_set.call_count >= size)

                # check_for called with correct parameter
                mock_check_for.assert_called_once()
                self.assertIn("workflow1", str(mock_check_for.call_args_list))

            # mock_get_one should be called exactly len(ex_path)+1 times
            size = 1
            for _ in ex_path.iterdir():
                size += 1
            self.assertTrue(mock_get_one.call_count >= size)

    def test_get_names_of_workflows_and_config_files1(self):
        # Arrange
        workflow_values = [
            ("workflow1", "wffile1"),
            ("workflow1", "wffile2"),
            ("workflow1", "wffile3"),
            ("workflow2", "wffile1"),
            ("workflow2", "wffile2"),
            ("workflow13", "wffile1"),
        ]
        result: Dict[str, List[str]]
        with patch.object(
            DatabaseTable, "get_multiple", return_value=workflow_values
        ) as mock_workflow_data:

            # Act
            result = self.workflow_data.get_names_of_workflows_and_config_files()

            # Assert
            mock_workflow_data.assert_called_once()
        self.assertEqual(len(result), 3)
        for key in result.keys():
            for file in result[key]:
                self.assertIn((key, file), workflow_values)

    def test_get_names_of_workflows_and_config_files2(self):
        # Arrange
        workflow_values = [("workflow1", "wffile1")]
        result: Dict[str, List[str]]
        with patch.object(
            DatabaseTable, "get_multiple", return_value=workflow_values
        ) as mock_workflow_data:

            # Act
            result = self.workflow_data.get_names_of_workflows_and_config_files()

            # Assert
            mock_workflow_data.assert_called_once()
        self.assertEqual(len(result), 1)
        for key in result.keys():
            for file in result[key]:
                self.assertIn((key, file), workflow_values)

    def test_get_names_of_workflows_and_config_files3(self):
        # empty database
        # Arrange
        workflow_values = []
        result: Dict[str, List[str]]
        with patch.object(
            DatabaseTable, "get_multiple", return_value=workflow_values
        ) as mock_workflow_data:

            # Act
            result = self.workflow_data.get_names_of_workflows_and_config_files()

            # Assert
            mock_workflow_data.assert_called_once()
        self.assertEqual(len(result), 0)
        for key in result.keys():
            for file in result[key]:
                self.assertIn((key, file), workflow_values)

    def test_create_new_version_of_workflow_instance(self):
        # NOTE: tests if the MySQL commands are doing what they're supposed to are not possible here.
        # Integration test needed

        # Arrange
        wf_name = "workflow1"
        version_number = VersionNumber("1.2")
        path = Path("./testfiles")
        new_version = DatabaseVersion(version_number, "note", path)
        old_version_number = "1"

        with patch.object(
            DatabaseTable,
            "get_one",
            return_value=(2,),
        ) as mock_get_one:
            with patch.object(
                DatabaseTable,
                "set",
            ) as mock_set:

                # Act
                self.workflow_data.create_new_version_of_workflow_instance(
                    wf_name, new_version, old_version_number
                )

                # Assert

                # Assert that correct parameters were used somewhere
                arg_list = mock_set.call_args_list
                i = 0
                # first call of set is for setting new version of workflow
                self.assertIn(wf_name, str(arg_list[i]))
                self.assertIn(version_number.get_number(), str(arg_list[i]))
                i += 1
                # two calls per file. Insert into ConfFile and insert into Versionfile
                for file in path.iterdir():
                    self.assertIn(file.name, str(arg_list[i]))
                    i += 1
                    self.assertIn(file.name, str(arg_list[i]))
                    i += 1

            arg_list = mock_get_one.call_args_list
            i = 0
            # get key calls for workflow name
            # new version
            self.assertIn(wf_name, str(arg_list[i]))
            self.assertIn(version_number.get_number(), str(arg_list[i]))
            i += 1
            # old version
            self.assertIn(wf_name, str(arg_list[i]))
            self.assertIn(old_version_number, str(arg_list[i]))
            i += 1
            # file
            for file in path.iterdir():
                self.assertIn(file.name, str(arg_list[i]))
                i += 1

    def test_get_config_file_from_workflow_instance(self):
        # Arrange
        wf_name = "workflow1"
        conf_name = "config_file name"
        version = "1"
        planed_result = Path("path")

        with patch.object(
            DatabaseTable, "get_one", return_value=(planed_result.name,)
        ) as mock_get_one:
            # Act
            result = self.workflow_data.get_config_file_from_workflow_instance(
                wf_name, conf_name, version
            )

            # Assert
            mock_get_one.assert_called()
            self.assertEqual(planed_result, result)

    def test_get_active_version_of_workflow_instance1(self):
        # test if workflow is in database
        # Arrange
        wf_name = "workflow1"
        version = "1_1_2_3"

        with patch.object(
            DatabaseTable, "get_one", return_value=(version,)
        ) as mock_get_one:
            # Act
            result = self.workflow_data.get_active_version_of_workflow_instance(wf_name)

            # Assert
            self.assertEqual(result, version)
            mock_get_one.assert_called_once()

    def test_get_active_version_of_workflow_instance2(self):
        # test if workflow is NOT in database
        # Arrange
        wf_name = "workflow1"
        version = "1_1_2_3"

        with patch.object(
            DatabaseTable,
            "get_one",
            return_value=version,
        ) as mock_get_one:
            mock_get_one.side_effect = InternalException("Error msg")
            with self.assertRaises(InternalException) as error:
                self.assertRaises(
                    InternalException,
                    self.workflow_data.get_active_version_of_workflow_instance(wf_name),
                )

    def test_get_config_file_from_active_workflow_instance(self):
        # relies on get_active_version_of_workflow_instance

        # Arrange
        wf_name = "workflow1"
        conf_name = "file name"
        conf_path = Path("file path")
        with patch.object(
            DatabaseTable, "get_one", return_value=(conf_path.name,)
        ) as mock_get_one:
            with patch.object(
                WorkflowData,
                "get_active_version_of_workflow_instance",
                return_value="1.1",
            ) as mock_get_active_version:
                # Act
                result = (
                    self.workflow_data.get_config_file_from_active_workflow_instance(
                        wf_name, conf_name
                    )
                )

                # Assert
                self.assertEqual(result, conf_path)
                # Assert functions used
                mock_get_active_version.assert_called_once()
                mock_get_one.assert_called()
                # Assert arguments in query
                call_args = str(mock_get_one.call_args_list)
                self.assertIn(wf_name, call_args)
                self.assertIn(conf_name, call_args)
