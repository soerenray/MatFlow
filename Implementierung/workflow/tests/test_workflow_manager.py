import filecmp
import os
import shutil
from typing import List
import mock
from pathlib import Path
from unittest import TestCase
from Implementierung.workflow.workflow_manager import WorkflowManager
from Implementierung.workflow.reduced_config_file import ReducedConfigFile
from Implementierung.workflow.database_version import DatabaseVersion
from Implementierung.workflow.frontend_version import FrontendVersion
from Implementierung.workflow.parameter_change import ParameterChange
from Implementierung.workflow.version_number import VersionNumber
from Implementierung.workflow.template import Template
from Implementierung.ExceptionPackage.MatFlowException import (
    DoubleTemplateNameException,
    InternalException,
    DoubleWorkflowInstanceNameException,
    EmptyConfigFolderException,
)


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
        expected_path: Path = (
            self.w_man._WorkflowManager__template_base_directory / "t1.py"
        )
        self.assertTrue(os.path.isfile(expected_path))
        # check if the content of the file was successfully copied
        self.assertTrue(filecmp.cmp(self.dag_file_t1, expected_path))

    # test double template exception
    def test_create_template_twice(self):
        # Act + Assert
        self.w_man.create_template(self.t1)
        self.assertRaises(
            DoubleTemplateNameException, self.w_man.create_template, self.t1
        )

    # test creating two differently named templates
    def test_create_two_templates(self):
        # Arrange
        t2: Template = Template("t2", self.dag_file_t1)

        # Act
        self.w_man.create_template(self.t1)
        self.w_man.create_template(t2)

        # Assert
        # check if the expected files exist
        self.assertTrue(
            "t1.py" in os.listdir(self.w_man._WorkflowManager__template_base_directory)
        )
        self.assertTrue(
            "t2.py" in os.listdir(self.w_man._WorkflowManager__template_base_directory)
        )


class TestCreateInstanceFromTemplate(TestWorkflowManager):
    def setUp(self):
        # create a possible template, that can be used for creation
        dag_file_t1: Path = self.base_path / "tpl1.py"
        self.name_t1: str = "t1"
        t1: Template = Template("t1", dag_file_t1)
        self.w_man.create_template(t1)

        # set up the base path for the conf folders
        self.conf_base_path: Path = self.base_path / "conf_folders"

    @mock.patch("Implementierung.workflow.workflow_manager.WorkflowData")
    def test_unknown_template_name(self, mock_wf_data):
        # Arrange
        unknown_name: str = "unknown"
        conf_folder: Path = self.conf_base_path / "folder1"
        expected_msg: str = (
            "Internal Error: " + unknown_name + " isn't a known template name."
        )

        # insert the mock object in the right attribute
        self.w_man._WorkflowManager__workflow_data = mock_wf_data

        # Act + Assert
        with self.assertRaises(InternalException) as context:
            self.w_man.create_workflow_instance_from_template(
                unknown_name, "instance", conf_folder
            )
        self.assertTrue(expected_msg in str(context.exception))

        # test that the database interface wasn't called
        self.assertFalse(mock_wf_data.create_wf_instance.called)

    @mock.patch("Implementierung.workflow.workflow_manager.WorkflowData")
    def test_valid_only_conf_files(self, mock_wf_data):
        # a valid creation, the config folder only consisting of conf-files
        # Arrange
        instance_name: str = "instance1"
        conf_folder: Path = self.conf_base_path / "folder1"

        # insert the mock object in the right attribute
        self.w_man._WorkflowManager__workflow_data = mock_wf_data

        # Act
        self.w_man.create_workflow_instance_from_template(
            self.name_t1, instance_name, conf_folder
        )

        # Assert
        # was there a dir for the instance created?
        expected_instance_path: Path = (
            self.w_man._WorkflowManager__versions_base_directory / instance_name
        )
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

    @mock.patch("Implementierung.workflow.workflow_manager.WorkflowData")
    def test_empty_config_folder(self, mock_wf_data):
        # Arrange
        instance_name: str = "instance1"
        conf_folder: Path = self.conf_base_path / "empty_folder"

        # insert the mock object in the right attribute
        self.w_man._WorkflowManager__workflow_data = mock_wf_data

        # Act + Assert
        self.assertRaises(
            EmptyConfigFolderException,
            self.w_man.create_workflow_instance_from_template,
            self.name_t1,
            instance_name,
            conf_folder,
        )

        # test that the database interface wasn't called
        self.assertFalse(mock_wf_data.create_wf_instance.called)

    @mock.patch("Implementierung.workflow.workflow_manager.WorkflowData")
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
        self.w_man.create_workflow_instance_from_template(
            self.name_t1, instance_name, conf_folder
        )

        # make sure the database interface was called exactly once
        self.assertEqual(mock_wf_data.create_wf_instance.call_count, 1)

        # now we expect an exception
        self.assertRaises(
            DoubleWorkflowInstanceNameException,
            self.w_man.create_workflow_instance_from_template,
            self.name_t1,
            instance_name,
            conf_folder,
        )

        # test that the database interface was only called the first time (the call_count doesn't change)
        self.assertEqual(mock_wf_data.create_wf_instance.call_count, 1)

    @mock.patch("Implementierung.workflow.workflow_manager.WorkflowData")
    def test_valid_mixed_files(self, mock_wf_data):
        # a valid creation, the config folder only consisting of conf-files as well as other files
        # Arrange
        instance_name: str = "instance2"
        conf_folder: Path = self.conf_base_path / "folder2"
        only_conf_dir: Path = self.conf_base_path / "folder1"

        # insert the mock object in the right attribute
        self.w_man._WorkflowManager__workflow_data = mock_wf_data

        # Act
        self.w_man.create_workflow_instance_from_template(
            self.name_t1, instance_name, conf_folder
        )

        # Assert
        # was there a dir for the instance created?
        expected_instance_path: Path = (
            self.w_man._WorkflowManager__versions_base_directory / instance_name
        )
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
        self.dag_file: Path = self.base_path / "tpl1.py"
        t1: Template = Template("t1", self.dag_file)
        self.t2: Template = Template("t2", self.dag_file)
        t3: Template = Template("t3", self.dag_file)
        self.w_man.create_template(t1)
        self.w_man.create_template(self.t2)
        self.w_man.create_template(t3)

    def test_get_template_names(self):
        # Arrange
        expected_names: List[str] = ["t1", "t2", "t3"]

        # Act
        actual_names: List[str] = self.w_man.get_template_names()

        # Assert
        self.assertEqual(expected_names, actual_names)

    def test_get_template_from_wrong_name(self):
        # Arrange
        wrong_name: str = "wrong_template"
        expected_msg: str = (
            "Internal Error: Selected template: " + wrong_name + " doesn't exist."
        )

        # Act + Assert
        with self.assertRaises(InternalException) as context:
            self.w_man.get_template_from_name(wrong_name)
        self.assertTrue(expected_msg in str(context.exception))

    def test_get_template_from_name(self):
        # Arrange
        template_name: str = "t2"
        expected_template: Template = self.t2

        # Act
        actual_template: Template = self.w_man.get_template_from_name(template_name)

        # Assert
        # compare templates by comparing their attributes
        self.assertEqual(expected_template.get_name(), actual_template.get_name())
        self.assertEqual(
            expected_template.get_dag_definition_file(),
            actual_template.get_dag_definition_file(),
        )


class TestCreateNewVersion(TestWorkflowManager):
    @mock.patch("Implementierung.workflow.workflow_manager.WorkflowData")
    def setUp(self, mock_wf_data):
        # create a template first
        dag_file_t1: Path = self.base_path / "tpl1.py"
        t1: Template = Template("t1", dag_file_t1)
        self.w_man.create_template(t1)

        # then create a workflow instance
        self.instance_name: str = "instance1"
        self.instance_path: Path = (
            self.w_man._WorkflowManager__versions_base_directory / self.instance_name
        )
        conf_folder: Path = self.base_path / "conf_folders" / "create_version"

        # for the actual creation we use a mock to avoid side effects
        self.w_man._WorkflowManager__workflow_data = mock_wf_data
        self.w_man.create_workflow_instance_from_template(
            "t1", self.instance_name, conf_folder
        )

        # apart from that we need actual updates for our files in form of ReducedConfigFiles
        name_config1: str = "test1"
        name_config2: str = "test2"
        self.file1_v1_1: ReducedConfigFile = ReducedConfigFile(
            name_config1, [("i_was", "changed"), ("key2", "value2"), ("me", "too")]
        )
        self.file2_v1_1: ReducedConfigFile = ReducedConfigFile(
            name_config2, [("key4", "value4"), ("key55", "value55"), ("key6", "6")]
        )
        self.file1_v1_2: ReducedConfigFile = ReducedConfigFile(
            name_config1, [("version", "1_2"), ("key2", "value2"), ("key3", "value3")]
        )
        self.file1_v1_1_1: ReducedConfigFile = ReducedConfigFile(
            name_config1, [("version", "1_1_1"), ("key2", "value2"), ("me", "too")]
        )
        self.version_note: str = "empty note"

    @mock.patch("Implementierung.workflow.workflow_manager.WorkflowData")
    def test_unknown_instance(self, mock_wf_data):
        # Arrange
        unknown_instance_name: str = "unknown"
        expected_msg: str = (
            "Internal Error: "
            + unknown_instance_name
            + " doesn't refer to a wf instance."
        )
        mock_wf_data.get_active_version_of_workflow_instance.return_value = "1"

        # insert the mock object in the right attribute
        self.w_man._WorkflowManager__workflow_data = mock_wf_data

        # Act + Assert
        with self.assertRaises(InternalException) as context:
            self.w_man.create_new_version_of_workflow_instance(
                unknown_instance_name, [self.file1_v1_1], self.version_note
            )
        self.assertTrue(expected_msg in str(context.exception))

        # make sure the database wasn't called
        self.assertFalse(mock_wf_data.called)

    @mock.patch("Implementierung.workflow.workflow_manager.WorkflowData")
    def test_create_multiple_versions(self, mock_wf_data):
        # in this test everything is supposed to go right. versions 1.1, 1.2, 1.1.1 are subsequently created
        # Arrange v1_1
        self.w_man._WorkflowManager__workflow_data = mock_wf_data
        mock_wf_data.get_active_version_of_workflow_instance.return_value = "1"
        mock_wf_data.get_version_numbers_of_workflow_instance.return_value = ["1"]

        # Act v1_1
        self.w_man.create_new_version_of_workflow_instance(
            self.instance_name, [self.file1_v1_1, self.file2_v1_1], self.version_note
        )

        # Assert v1_1
        self.assertTrue(mock_wf_data.create_new_version_of_workflow_instance.called)

        # Arrange v1_2
        mock_wf_data.get_active_version_of_workflow_instance.return_value = "1"
        mock_wf_data.get_version_numbers_of_workflow_instance.return_value = [
            "1",
            "1.1",
        ]

        # Act v1_2
        self.w_man.create_new_version_of_workflow_instance(
            self.instance_name, [self.file1_v1_2], self.version_note
        )

        # Assert v1_2
        self.assertTrue(mock_wf_data.create_new_version_of_workflow_instance.called)

        # Arrange v1_1_1
        mock_wf_data.get_active_version_of_workflow_instance.return_value = "1.1"
        mock_wf_data.get_version_numbers_of_workflow_instance.return_value = [
            "1",
            "1.1",
            "1.2",
        ]

        # Act v1_1_1
        self.w_man.create_new_version_of_workflow_instance(
            self.instance_name, [self.file1_v1_1_1], self.version_note
        )

        # Assert v1_1_1
        self.assertTrue(mock_wf_data.create_new_version_of_workflow_instance.called)

        # Assert Directory and file creations
        # No need to test all the files internally because that functionality was tested in ConfigFile already
        path1_1: Path = self.instance_path / "1_1"
        self.assertTrue(os.path.isdir(path1_1))
        self.assertTrue(os.path.isfile(path1_1 / "test1.conf"))
        self.assertTrue(os.path.isfile(path1_1 / "test2.conf"))
        path1_2: Path = self.instance_path / "1_2"
        self.assertTrue(os.path.isdir(path1_2))
        self.assertTrue(os.path.isfile(path1_2 / "test1.conf"))
        self.assertFalse(
            os.path.isfile(path1_2 / "test2.conf")
        )  # this file shouldn't exist, it wasn't changed
        path1_1_1: Path = self.instance_path / "1_1_1"
        self.assertTrue(os.path.isdir(path1_1_1))
        self.assertTrue(os.path.isfile(path1_1_1 / "test1.conf"))
        self.assertFalse(
            os.path.isfile(path1_1_1 / "test2.conf")
        )  # this file shouldn't exist, it wasn't changed


class TestGetVersionsFromWorkflowInstance(TestWorkflowManager):
    def setUp(self):
        # we want to work on an instance with multiple versions for that there is a dir prepared
        prepared_folder: Path = self.base_path / "wf_instances_prepared"
        self.w_man._WorkflowManager__versions_base_directory = prepared_folder
        # now the folder is set up
        # now we have to create the DatabaseVersion that are returned from the database mock
        self.instance_path: Path = prepared_folder / "instance1"
        self.ver1: DatabaseVersion = DatabaseVersion(
            VersionNumber("1"), "", self.instance_path / "1"
        )
        self.ver1_1: DatabaseVersion = DatabaseVersion(
            VersionNumber("1.1"), "", self.instance_path / "1_1"
        )
        self.ver1_2: DatabaseVersion = DatabaseVersion(
            VersionNumber("1.2"), "", self.instance_path / "1_2"
        )
        self.ver1_1_1: DatabaseVersion = DatabaseVersion(
            VersionNumber("1.1.1"), "", self.instance_path / "1_1_1"
        )

    def tearDown(self):
        # now we have to put in the old, empty instance folder
        empty_folder: Path = self.base_path / "wf_instances"
        self.w_man._WorkflowManager__versions_base_directory = empty_folder

    @mock.patch("Implementierung.workflow.workflow_manager.WorkflowData")
    def test_unknown_instance(self, mock_wf_data):
        # Arrange
        unknown_instance_name: str = "unknown"
        self.w_man._WorkflowManager__workflow_data = mock_wf_data
        expected_msg: str = (
            "Internal Error: "
            + unknown_instance_name
            + " doesn't refer to a wf instance."
        )

        # Act + Assert
        with self.assertRaises(InternalException) as context:
            self.w_man.get_versions_from_workflow_instance(unknown_instance_name)
        self.assertTrue(expected_msg in str(context.exception))

        # make sure the database wasn't called
        self.assertFalse(mock_wf_data.called)

    @mock.patch("Implementierung.workflow.workflow_manager.WorkflowData")
    def test_valid_instance(self, mock_wf_data):
        # Arrange
        instance_name: str = "instance1"

        # define small mock function for 'dynamic' return values
        def file_from_version(wf_name: str, conf_name: str, version: str):
            if conf_name == "test1" or version in ["1", "1.1"]:
                return (
                    self.instance_path
                    / VersionNumber(version).get_dir_name()
                    / conf_name
                )
            else:
                return (
                    self.instance_path
                    / VersionNumber(version).get_predecessor().get_dir_name()
                    / conf_name
                )

        mock_wf_data.get_config_file_from_workflow_instance.side_effect = (
            file_from_version
        )
        mock_wf_data.get_database_versions_of_workflow_instance.return_value = [
            self.ver1,
            self.ver1_1,
            self.ver1_1_1,
            self.ver1_2,
        ]
        self.w_man._WorkflowManager__workflow_data = mock_wf_data

        # Act
        frontend_versions: List[
            FrontendVersion
        ] = self.w_man.get_versions_from_workflow_instance(instance_name)

        # Assert
        # we don't have to inspect the FrontendVersions themselves (we tested that in DatabaseVersion)
        # but rather look that all of them are there in the right order
        self.assertEqual(3, len(frontend_versions))
        self.assertEqual("1.1", frontend_versions[0].get_version_number().get_number())
        self.assertEqual(
            "1.1.1", frontend_versions[1].get_version_number().get_number()
        )
        self.assertEqual("1.2", frontend_versions[2].get_version_number().get_number())


class TestCopyFilesWithExtension(TestWorkflowManager):
    base_path_copy_whole_dir: Path = Path(
        "test_files/workflow_manager/copyFilesWithExtension"
    )
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
        self.w_man._WorkflowManager__copy_files_with_extension(
            src_path, self.dst_dir, ""
        )

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
        self.w_man._WorkflowManager__copy_files_with_extension(
            src_path, self.dst_dir, ".conf"
        )

        # Assert
        self.assertTrue(are_dir_trees_equal(src_extension_filtered, self.dst_dir))

    def test_copy_any_files(self):
        # Arrange
        src_path: Path = self.base_path_copy_whole_dir / "src3"

        # Act
        self.w_man._WorkflowManager__copy_files_with_extension(
            src_path, self.dst_dir, ""
        )

        # Assert
        self.assertTrue(are_dir_trees_equal(src_path, self.dst_dir))


def are_dir_trees_equal(dir1: Path, dir2: Path) -> bool:
    dirs_cmp = filecmp.dircmp(dir1, dir2)
    if (
        len(dirs_cmp.left_only) > 0
        or len(dirs_cmp.right_only) > 0
        or len(dirs_cmp.funny_files) > 0
    ):
        return False
    (_, mismatch, errors) = filecmp.cmpfiles(
        dir1, dir2, dirs_cmp.common_files, shallow=False
    )
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
