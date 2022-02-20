import unittest
from pathlib import Path
from unittest.mock import patch, Mock

from matflow.database.WorkflowData import WorkflowData
from matflow.workflow.workflow_instance import WorkflowInstance
from matflow.database.DatabaseTable import DatabaseTable


class TestWorkflowDataSetup(unittest.TestCase):
    workflow_data: WorkflowData

    def setUp(self) -> None:
        self.workflow_data = WorkflowData.get_instance()


class TestWorkflowData(TestWorkflowDataSetup):
    def test_get_Instance(self):
        self.assertEqual(self.workflow_data, WorkflowData.get_instance())

    """def test_create_wf_instance(self):
        with patch('DatabaseTable.get_one') as mock_database:
            mock_database.get_one().return_value = 1
            with patch('DatabaseTable.get_one') as mock_workflow_version_key_get:
                # Arrange
                workflow = WorkflowInstance("workflow1", Path(".test"), Path("."))
                ex_path = Path(".")

                # Act
                self.workflow_data.create_wf_instance(workflow, ex_path)

                # Assert
                mock_database



        self.assertEqual(True, True)"""
