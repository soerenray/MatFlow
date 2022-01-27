import filecmp
import os
from pathlib import Path
from typing import Union, Any
from unittest import TestCase
from Implementierung.workflow.workflow_manager import WorkflowManager


class TestWorkflowManager(TestCase):
    pass
#     w_man: WorkflowManager
#
#     def setUp(self):
#         self.w_man = WorkflowManager.get_instance()
#         other_w_man: WorkflowManager = WorkflowManager.get_instance()
#         self.assertEqual(self.w_man, other_w_man)


class TestCreateNewVersion(TestWorkflowManager):
    pass


class TestGetVersionsFromWorkflowInstance(TestWorkflowManager):
    pass


class TestCopyWholeDir(TestWorkflowManager):
    base_dir: Path = Path("test_files/workflow_manager/copyWholeDir")

    # before testing the actual method "copy_whole_dir" I want to make sure the method "are_dir_trees_equal" that is
    # used for testing works fine itself
    def test_are_dir_trees_equal_diff_dirs(self):
        # in this test I compare dirs with different tree structure
        # Arrange
        dir1: Path = self.base_dir
        dir2: Path = self.base_dir / "src2"

        # Act
        equal: bool = are_dir_trees_equal(dir1, dir2)

        # Assert
        self.assertFalse(equal)

    def test_are_dir_trees_equal_same_dir(self):
        # in this test I compare a dir to itself
        # Arrange
        dir1: Path = self.base_dir / "src2"
        dir2: Path = self.base_dir / "src2"

        # Act
        equal: bool = are_dir_trees_equal(dir1, dir2)

        # Assert
        self.assertTrue(equal)

    def test_are_dir_trees_equal_same_tree_diff_file(self):
        # in this test I compare a dir to itself
        # Arrange
        dir1: Path = self.base_dir / "src3"
        dir2: Path = self.base_dir / "src3_changed_file"

        # Act
        equal: bool = are_dir_trees_equal(dir1, dir2)

        # Assert
        self.assertFalse(equal)

    def test_are_dir_trees_equal_diff_but_equal_dirs(self):
        # in this test I compare a dir to itself
        # Arrange
        dir1: Path = self.base_dir / "src3"
        dir2: Path = self.base_dir / "src3_copy"

        # Act
        equal: bool = are_dir_trees_equal(dir1, dir2)

        # Assert
        self.assertTrue(equal)

    # now we can start with the tests for the actual method


def are_dir_trees_equal(dir1: Path, dir2: Path) -> bool:
    dirs_cmp = filecmp.dircmp(dir1, dir2)
    if len(dirs_cmp.left_only) > 0 or len(dirs_cmp.right_only) > 0 or \
            len(dirs_cmp.funny_files) > 0:
        return False
    (_, mismatch, errors) = filecmp.cmpfiles(
        dir1, dir2, dirs_cmp.common_files, shallow=False)
    if len(mismatch) > 0 or len(errors) > 0:
        return False
    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = dir1 / common_dir
        new_dir2 = dir2 / common_dir
        if not are_dir_trees_equal(new_dir1, new_dir2):
            return False
    return True
