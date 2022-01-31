import filecmp
import os
import shutil
from typing import List

import mock
from pathlib import Path
from unittest import TestCase
from Implementierung.workflow.workflow_manager import WorkflowManager
from Implementierung.workflow.template import Template
from Implementierung.ExceptionPackage.MatFlowException import DoubleTemplateNameException, InternalException, \
    DoubleWorkflowInstanceNameException, EmptyConfigFolderException
from Implementierung.Database.WorkflowData import WorkflowData


class TestWorkflowManager(TestCase):
    base_path: Path = Path("test_files/workflow_manager")
    w_man: WorkflowManager = WorkflowManager.get_instance()
    w_man._WorkflowManager__versions_base_directory = base_path / "wf_instances"
    w_man._WorkflowManager__template_base_directory = base_path / "templates"

    def tearDown(self):
        # clean up dirs after every run
        delete_dir_content(self.w_man._WorkflowManager__template_base_directory)
        delete_dir_content(self.w_man._WorkflowManager__versions_base_directory)


class TestCreateTemplate(TestWorkflowManager):
    def setUp(self):
        self.dag_file_t1: Path = self.base_path / "tpl1.py"
        self.t1: Template = Template("t1", self.dag_file_t1)

    # create valid template
    def test_create_valid_template(self):
        # Act
        self.w_man.create_template(self.t1)

        # Assert
        # check if the file was inserted at the right place
        expected_path: Path = self.w_man._WorkflowManager__template_base_directory / "t1.py"
        self.assertTrue(os.path.isfile(expected_path))
        # check if the content of the file was successfully copied
        self.assertTrue(filecmp.cmp(self.dag_file_t1, expected_path))

    # test double template exception
    def test_create_template_twice(self):
        # Act + Assert
        self.w_man.create_template(self.t1)
        self.assertRaises(DoubleTemplateNameException, self.w_man.create_template, self.t1)

    # test creating two differently named templates
    def test_create_two_templates(self):
        # Arrange
        t2: Template = Template("t2", self.dag_file_t1)

        # Act
        self.w_man.create_template(self.t1)
        self.w_man.create_template(t2)

        # Assert
        # check if the expected files exist
        self.assertTrue("t1.py" in os.listdir(self.w_man._WorkflowManager__template_base_directory))
        self.assertTrue("t2.py" in os.listdir(self.w_man._WorkflowManager__template_base_directory))


class TestCreateInstanceFromTemplate(TestWorkflowManager):
    def setUp(self):
        # create a possible template, that can be used for creation
        dag_file_t1: Path = self.base_path / "tpl1.py"
        self.name_t1: str = "t1"
        t1: Template = Template("t1", dag_file_t1)
        self.w_man.create_template(t1)

        # set up the base path for the conf folders
        self.conf_base_path: Path = self.base_path / "conf_folders"

    @mock.patch('Implementierung.workflow.workflow_manager.WorkflowData')
    def test_unknown_template_name(self, mock_wf_data):
        # Arrange
        unknown_name: str = "unknown"
        conf_folder: Path = self.conf_base_path / "folder1"
        expected_msg: str = "Internal Error: " + unknown_name + " isn't a known template name."

        # insert the mock object in the right attribute
        self.w_man._WorkflowManager__workflow_data = mock_wf_data

        # Act + Assert
        with self.assertRaises(InternalException) as context:
            self.w_man.create_workflow_instance_from_template(unknown_name, "instance", conf_folder)
        self.assertTrue(expected_msg in str(context.exception))

        # test that the database interface wasn't called
        self.assertFalse(mock_wf_data.create_wf_instance.called)

    @mock.patch('Implementierung.workflow.workflow_manager.WorkflowData')
    def test_valid_only_conf_files(self, mock_wf_data):
        # a valid creation, the config folder only consisting of conf-files
        # Arrange
        instance_name: str = "instance1"
        conf_folder: Path = self.conf_base_path / "folder1"

        # insert the mock object in the right attribute
        self.w_man._WorkflowManager__workflow_data = mock_wf_data

        # Act
        self.w_man.create_workflow_instance_from_template(self.name_t1, instance_name, conf_folder)

        # Assert
        # was there a dir for the instance created?
        expected_instance_path: Path = self.w_man._WorkflowManager__versions_base_directory / instance_name
        self.assertTrue(os.path.isdir(expected_instance_path))

        # test that the database interface was called
        self.assertTrue(mock_wf_data.create_wf_instance.called)

        # is there a "current_conf"-dir underneath, mirroring the ingoing folder?
        expected_path: Path = expected_instance_path / "current_conf"
        self.assertTrue(os.path.isdir(expected_path))
        self.assertTrue(are_dir_trees_equal(expected_path, conf_folder))

        # is there a "1"-dir underneath the instance dir that contains only the conf-files of the ingoing folder?
        expected_path: Path = expected_instance_path / "1"
        self.assertTrue(os.path.isdir(expected_path))
        self.assertTrue(are_dir_trees_equal(expected_path, conf_folder))

    @mock.patch('Implementierung.workflow.workflow_manager.WorkflowData')
    def test_empty_config_folder(self, mock_wf_data):
        # Arrange
        instance_name: str = "instance1"
        conf_folder: Path = self.conf_base_path / "empty_folder"

        # insert the mock object in the right attribute
        self.w_man._WorkflowManager__workflow_data = mock_wf_data

        # Act + Assert
        self.assertRaises(EmptyConfigFolderException, self.w_man.create_workflow_instance_from_template,
                          self.name_t1, instance_name, conf_folder)

        # test that the database interface wasn't called
        self.assertFalse(mock_wf_data.create_wf_instance.called)

    @mock.patch('Implementierung.workflow.workflow_manager.WorkflowData')
    def test_double_instance_name(self, mock_wf_data):
        # first repeat 'test_valid_only_conf_files' from above without testing, then try to create the same instance
        # again -> should raise a DoubleWorkflowInstanceNameException
        # Arrange
        instance_name: str = "instance1"
        conf_folder: Path = self.conf_base_path / "folder1"

        # insert the mock object in the right attribute
        self.w_man._WorkflowManager__workflow_data = mock_wf_data

        # Act + Assert
        # creating the first instance goes well
        self.w_man.create_workflow_instance_from_template(self.name_t1, instance_name, conf_folder)

        # make sure the database interface was called exactly once
        self.assertEqual(mock_wf_data.create_wf_instance.call_count, 1)

        # now we expect an exception
        self.assertRaises(DoubleWorkflowInstanceNameException, self.w_man.create_workflow_instance_from_template,
                          self.name_t1, instance_name, conf_folder)

        # test that the database interface was only called the first time (the call_count doesn't change)
        self.assertEqual(mock_wf_data.create_wf_instance.call_count, 1)

    @mock.patch('Implementierung.workflow.workflow_manager.WorkflowData')
    def test_valid_mixed_files(self, mock_wf_data):
        # a valid creation, the config folder only consisting of conf-files as well as other files
        # Arrange
        instance_name: str = "instance2"
        conf_folder: Path = self.conf_base_path / "folder2"
        only_conf_dir: Path = self.conf_base_path / "folder1"

        # insert the mock object in the right attribute
        self.w_man._WorkflowManager__workflow_data = mock_wf_data

        # Act
        self.w_man.create_workflow_instance_from_template(self.name_t1, instance_name, conf_folder)

        # Assert
        # was there a dir for the instance created?
        expected_instance_path: Path = self.w_man._WorkflowManager__versions_base_directory / instance_name
        self.assertTrue(os.path.isdir(expected_instance_path))

        # test that the database interface was called
        self.assertTrue(mock_wf_data.create_wf_instance.called)

        # is there a "current_conf"-dir underneath, mirroring the ingoing folder?
        expected_path: Path = expected_instance_path / "current_conf"
        self.assertTrue(os.path.isdir(expected_path))
        self.assertTrue(are_dir_trees_equal(expected_path, conf_folder))

        # is there a "1"-dir underneath the instance dir that contains only the conf-files of the ingoing folder?
        expected_path: Path = expected_instance_path / "1"
        self.assertTrue(os.path.isdir(expected_path))
        self.assertTrue(are_dir_trees_equal(expected_path, only_conf_dir))


class TestGetTemplateAndNames(TestWorkflowManager):
    def setUp(self):
        # create tree different templates
        dag_file: Path = self.base_path / "tpl1.py"
        t1: Template = Template("t1", dag_file)
        t2: Template = Template("t2", dag_file)
        t3: Template = Template("t3", dag_file)
        self.w_man.create_template(t1)
        self.w_man.create_template(t2)
        self.w_man.create_template(t3)

    def test_get_template_names(self):
        # Arrange
        expected_names: List[str] = ["t1", "t2", "t3"]

        # Act
        actual_names: List[str] = self.w_man.get_template_names()

        # Assert
        self.assertEqual(expected_names, actual_names)


class TestCreateNewVersion(TestWorkflowManager):
    pass


class TestGetVersionsFromWorkflowInstance(TestWorkflowManager):
    pass


class TestCopyFilesWithExtension(TestWorkflowManager):
    base_path_copy_whole_dir: Path = Path("test_files/workflow_manager/copyFilesWithExtension")
    dst_dir: Path = base_path_copy_whole_dir / "dst"

    def setUp(self):
        # always clear the destination directory
        if os.path.exists(self.dst_dir):
            shutil.rmtree(self.dst_dir)

    # before testing the actual method "copy_whole_dir" I want to make sure the method "are_dir_trees_equal" that is
    # used for testing works fine itself
    def test_are_dir_trees_equal_diff_dirs(self):
        # in this test I compare dirs with different tree structure
        # Arrange
        dir1: Path = self.base_path_copy_whole_dir
        dir2: Path = self.base_path_copy_whole_dir / "src2"

        # Act
        equal: bool = are_dir_trees_equal(dir1, dir2)

        # Assert
        self.assertFalse(equal)

    def test_are_dir_trees_equal_same_dir(self):
        # in this test I compare a dir to itself
        # Arrange
        dir1: Path = self.base_path_copy_whole_dir / "src2"
        dir2: Path = self.base_path_copy_whole_dir / "src2"

        # Act
        equal: bool = are_dir_trees_equal(dir1, dir2)

        # Assert
        self.assertTrue(equal)

    def test_are_dir_trees_equal_same_tree_diff_file(self):
        # in this test I compare a dir to itself
        # Arrange
        dir1: Path = self.base_path_copy_whole_dir / "src3"
        dir2: Path = self.base_path_copy_whole_dir / "src3_changed_file"

        # Act
        equal: bool = are_dir_trees_equal(dir1, dir2)

        # Assert
        self.assertFalse(equal)

    def test_are_dir_trees_equal_diff_but_equal_dirs(self):
        # in this test I compare a dir to itself
        # Arrange
        dir1: Path = self.base_path_copy_whole_dir / "src3"
        dir2: Path = self.base_path_copy_whole_dir / "src3_copy"

        # Act
        equal: bool = are_dir_trees_equal(dir1, dir2)

        # Assert
        self.assertTrue(equal)

    # now we can start with the tests for the actual method
    def test_empty_dir(self):
        # Arrange
        src_path: Path = self.base_path_copy_whole_dir / "src1"

        # Act
        self.w_man._WorkflowManager__copy_files_with_extension(src_path, self.dst_dir, "")

        # Assert
        self.assertTrue(are_dir_trees_equal(src_path, self.dst_dir))

# this is no longer ment to work, the src directory has to be flat
#    def test_dir_with_subdir(self):
#        # Arrange
#        src_path: Path = self.base_path_copy_whole_dir / "src2"
#
#        # Act
#        self.w_man._WorkflowManager__copy_files_with_extension(src_path, self.dst_dir, "")
#
#        # Assert
#        self.assertTrue(are_dir_trees_equal(src_path, self.dst_dir))

    def test_dir_with_files(self):
        # Arrange
        src_path: Path = self.base_path_copy_whole_dir / "src3"
        src_extension_filtered: Path = self.base_path_copy_whole_dir / "src3_extension"

        # Act
        self.w_man._WorkflowManager__copy_files_with_extension(src_path, self.dst_dir, ".conf")

        # Assert
        self.assertTrue(are_dir_trees_equal(src_extension_filtered, self.dst_dir))

    def test_copy_any_files(self):
        # Arrange
        src_path: Path = self.base_path_copy_whole_dir / "src3"

        # Act
        self.w_man._WorkflowManager__copy_files_with_extension(src_path, self.dst_dir, "")

        # Assert
        self.assertTrue(are_dir_trees_equal(src_path, self.dst_dir))


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


def delete_dir_content(dir_path: Path):
    for content in os.listdir(dir_path):
        content_path: Path = dir_path / content
        if os.path.isfile(content_path) or os.path.islink(content_path):
            os.unlink(content_path)
        elif os.path.isdir(content_path):
            shutil.rmtree(content_path)
