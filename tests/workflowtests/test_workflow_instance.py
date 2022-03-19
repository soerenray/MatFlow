import os.path
import unittest
from pathlib import Path
from unittest.mock import patch

from matflow.workflow import workflow_instance
from matflow.workflow.workflow_instance import WorkflowInstance


class TestActivateInstance(unittest.TestCase):
    def setUp(self):
        base_path: Path = Path(__file__).parent.absolute()
        self.dag_path = Path(
            os.path.join(
                base_path, "test_files", "workflow_manager", "template1", "tpl1.py"
            )
        )
        config_path = Path(os.path.join(base_path, "test_files", "config_file"))
        self.instance = WorkflowInstance("test_instance", self.dag_path, config_path)

    def test_activate_instance_call(self):
        with patch.object(workflow_instance.shutil, "copyfile") as mock_method:
            self.instance.activate_instance(self.dag_path)
            assert mock_method.call_count > 0

    def test_activate_instance_(self):
        self.instance.activate_instance(self.dag_path)
        # if success: file in dags folder
        p = Path(__file__)
        # root -> test -> workflowtests -> test_workflow_instance.py
        dags_folder = os.path.join(Path(p.parent.parent.parent.absolute()), "dags")
        self.assertTrue(os.path.isfile(os.path.join(dags_folder, "test_instance.py")))
        os.remove(os.path.join(dags_folder, "test_instance.py"))
