import filecmp
from pathlib import Path
from typing import Union, Any
from unittest import TestCase
from workflow.workflow_manager import WorkflowManager


class TestWorkflowManager(TestCase):
    w_man: WorkflowManager

    def setUp(self):
        self.w_man = WorkflowManager.get_instance()
        other_w_man: WorkflowManager = WorkflowManager.get_instance()
        self.assertEqual(self.w_man, other_w_man)


class TestCreateNewVersion(TestWorkflowManager):
    pass


class TestGetVersionsFromWorkflowInstance(TestWorkflowManager):
    pass

class TestCopyWholeDir(TestWorkflowManager):
    base_dir: Path = Path("test_files/workflow_manager/copyWholeDir")


def are_dir_trees_equal(dir1: Path, dir2: Path) -> bool:
    dirs_cmp = filecmp.dircmp(dir1, dir2)
