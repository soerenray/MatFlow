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
        ex_path = Path(".")

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
