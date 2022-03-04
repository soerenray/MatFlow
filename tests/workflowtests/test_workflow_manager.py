import filecmp
import os
import shutil
import unittest
from typing import List
import unittest.mock as mock
from pathlib import Path
from unittest import TestCase
from matflow.database.DatabaseTable import DatabaseTable

with mock.patch.object(DatabaseTable, "get_instance", return_value=""):
    from matflow.workflow.workflow_manager import WorkflowManager
from matflow.workflow.reduced_config_file import ReducedConfigFile
from matflow.workflow.database_version import DatabaseVersion
from matflow.workflow.frontend_version import FrontendVersion
from matflow.workflow.version_number import VersionNumber
from matflow.workflow.template import Template
from matflow.exceptionpackage.MatFlowException import (
    DoubleTemplateNameException,
    InternalException,
    DoubleWorkflowInstanceNameException,
    EmptyConfigFolderException,
    WorkflowInstanceRunningException,
)


class TestWorkflowManager(TestCase):
    w_man: WorkflowManager
    base_path: Path
    temp_path: Path
    wf_path: Path

    # initialize WorkflowManager
    w_man: WorkflowManager = WorkflowManager.get_instance()

    # initialize paths
    base_path: Path = Path(__file__).parent / "test_files/workflow_manager"
    temp_path: Path = base_path / "templates"
    wf_path: Path = base_path / "wf_instances"

    # insert paths into WorkflowManager
    w_man._WorkflowManager__versions_base_directory = wf_path
    w_man._WorkflowManager__template_base_directory = temp_path

    def setUp(self):
        # make sure empty dirs exist (git doesn't allow to push them)
        conf_path: Path = self.base_path / "conf_folders"
        folders: List[Path] = [
            self.temp_path,
            self.wf_path,
            conf_path / "folder1",
            conf_path / "folder2",
            conf_path / "create_version",
            self.base_path / "template1",
        ]
        for folder in folders:
            if not os.path.isdir(folder):
                os.mkdir(folder)

        # restore deleted files
        files: List[Path] = [
            Path("template1") / "tpl1.py",
            Path("conf_folders") / "folder1" / "file1.conf",
            Path("conf_folders") / "folder1" / "file2.conf",
            Path("conf_folders") / "folder2" / "file1.conf",
            Path("conf_folders") / "folder2" / "file2.conf",
            Path("conf_folders") / "folder2" / "png_file.png",
            Path("conf_folders") / "create_version" / "test1.conf",
            Path("conf_folders") / "create_version" / "test2.conf",
        ]
        backup_path: Path = self.base_path / "backup_stuff"
        for file in files:
            if not os.path.isfile(self.base_path / file):
                shutil.copy(backup_path / file, self.base_path / file)

    def tearDown(self):
        # clean up dirs after every run
        delete_dir_content(self.temp_path)
        delete_dir_content(self.wf_path)


class TestCreateTemplate(TestWorkflowManager):
    def setUp(self):
        super(TestCreateTemplate, self).setUp()
        self.dag_file_t1: Path = self.base_path / "template1" / "tpl1.py"
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
        self.assertTrue(
            filecmp.cmp(
                make_path_to_backup(self.base_path, self.dag_file_t1), expected_path
            )
        )

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

        # restore the dag file
        os.mkdir(self.dag_file_t1.parent)
        shutil.copy(
            make_path_to_backup(self.base_path, self.dag_file_t1), self.dag_file_t1
        )

        # then create second template
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
        super(TestCreateInstanceFromTemplate, self).setUp()
        # create a possible template, that can be used for creation
        dag_file_t1: Path = self.base_path / "template1" / "tpl1.py"
        self.name_t1: str = "t1"
        t1: Template = Template("t1", dag_file_t1)
        self.w_man.create_template(t1)

        # set up the base path for the conf folders
        self.conf_base_path: Path = self.base_path / "conf_folders"

    @mock.patch("matflow.workflow.workflow_manager.WorkflowData")
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

    @mock.patch("matflow.workflow.workflow_manager.WorkflowData")
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
        self.assertTrue(
            are_dir_trees_equal(
                expected_path, make_path_to_backup(self.base_path, conf_folder)
            )
        )

        # is there a "1"-dir underneath the instance dir that contains only the conf-files of the ingoing folder?
        expected_path: Path = expected_instance_path / "1"
        self.assertTrue(os.path.isdir(expected_path))
        self.assertTrue(
            are_dir_trees_equal(
                expected_path, make_path_to_backup(self.base_path, conf_folder)
            )
        )

    # in theory test works but it's commented out because empty folders aren't a thing with git
    #    @mock.patch("matflow.workflow.workflow_manager.WorkflowData")
    #    def test_empty_config_folder(self, mock_wf_data):
    #        # Arrange
    #        instance_name: str = "instance1"
    #        conf_folder: Path = self.conf_base_path / "empty_folder"
    #
    #        # insert the mock object in the right attribute
    #        self.w_man._WorkflowManager__workflow_data = mock_wf_data
    #
    #        # Act + Assert
    #        self.assertRaises(
    #            EmptyConfigFolderException,
    #            self.w_man.create_workflow_instance_from_template,
    #            self.name_t1,
    #            instance_name,
    #            conf_folder,
    #        )
    #
    #        # test that the database interface wasn't called
    #        self.assertFalse(mock_wf_data.create_wf_instance.called)

    @mock.patch("matflow.workflow.workflow_manager.WorkflowData")
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

    @mock.patch("matflow.workflow.workflow_manager.WorkflowData")
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
        self.assertTrue(
            are_dir_trees_equal(
                expected_path, make_path_to_backup(self.base_path, conf_folder)
            )
        )

        # is there a "1"-dir underneath the instance dir that contains only the conf-files of the ingoing folder?
        expected_path: Path = expected_instance_path / "1"
        self.assertTrue(os.path.isdir(expected_path))
        self.assertTrue(
            are_dir_trees_equal(
                expected_path, make_path_to_backup(self.base_path, only_conf_dir)
            )
        )


class TestGetTemplateAndNames(TestWorkflowManager):
    def setUp(self):
        super(TestGetTemplateAndNames, self).setUp()
        # create tree different templates
        self.dag_file: Path = self.base_path / "template1" / "tpl1.py"
        t1: Template = Template("t1", self.dag_file)
        self.t2: Template = Template("t2", self.dag_file)
        t3: Template = Template("t3", self.dag_file)
        for template in [t1, self.t2, t3]:
            self.w_man.create_template(template)

            # restore the dag file
            os.mkdir(self.dag_file.parent)
            shutil.copy(
                make_path_to_backup(self.base_path, self.dag_file), self.dag_file
            )

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
    @mock.patch("matflow.workflow.workflow_manager.WorkflowData")
    def setUp(self, mock_wf_data):
        super(TestCreateNewVersion, self).setUp()
        # create a template first
        dag_file_t1: Path = self.base_path / "template1" / "tpl1.py"
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
        name_config1: str = "test1.conf"
        name_config2: str = "test2.conf"
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

    @mock.patch("matflow.workflow.workflow_manager.WorkflowData")
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

    @mock.patch("matflow.workflow.workflow_manager.WorkflowData")
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
        super(TestGetVersionsFromWorkflowInstance, self).setUp()
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

    @mock.patch("matflow.workflow.workflow_manager.WorkflowData")
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

    @mock.patch("matflow.workflow.workflow_manager.WorkflowData")
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


class TestSetActiveVersionByNumber(TestGetVersionsFromWorkflowInstance):
    # this class inherits from TestGetVersionsFromWorkflowInstance because we want the same setUp and tearDown methods

    @mock.patch.object(
        WorkflowManager, "_WorkflowManager__is_workflow_instance_running"
    )
    @mock.patch("matflow.workflow.workflow_manager.WorkflowData")
    def test_with_unknown_instance(self, mock_wf_data, mock_running):
        # Arrange
        # put the mock in place
        self.w_man._WorkflowManager__workflow_data = mock_wf_data
        unknown_instance_name: str = "unknown"
        any_number: str = ""  # should be irrelevant
        # make sure the mock method says the wf isn't running
        mock_running.return_value = False
        expected_msg: str = (
            "Internal Error: "
            + unknown_instance_name
            + " doesn't refer to a wf instance."
        )

        # Act + Assert
        with self.assertRaises(InternalException) as context:
            self.w_man.set_active_version_through_number(
                unknown_instance_name, any_number
            )
        self.assertTrue(expected_msg in str(context.exception))

        # assert no calls to the airflow api
        self.assertFalse(mock_running.called)
        # assert no calls to the database were made
        self.assertFalse(mock_wf_data.called)

    @mock.patch.object(
        WorkflowManager, "_WorkflowManager__is_workflow_instance_running"
    )
    @mock.patch("matflow.workflow.workflow_manager.WorkflowData")
    def test_while_instance_running(self, mock_wf_data, mock_running):
        # Arrange
        # put the mock in place
        self.w_man._WorkflowManager__workflow_data = mock_wf_data
        # make sure the mock method says the wf is running
        mock_running.return_value = True
        instance_name: str = "instance1"
        new_version: str = "1.1"

        # Act + Assert
        self.assertRaises(
            WorkflowInstanceRunningException,
            self.w_man.set_active_version_through_number,
            instance_name,
            new_version,
        )
        # assert no calls to the database were made
        self.assertFalse(mock_wf_data.called)

    @mock.patch.object(
        WorkflowManager, "_WorkflowManager__is_workflow_instance_running"
    )
    @mock.patch("matflow.workflow.workflow_manager.WorkflowData")
    def test_with_unknown_number(self, mock_wf_data, mock_running):
        # Arrange
        # put the mock in place
        self.w_man._WorkflowManager__workflow_data = mock_wf_data
        # make sure the mock method says the wf isn't running
        mock_running.return_value = False
        instance_name: str = "instance1"
        wrong_number: str = "1.5"  # actually there is no version 1.5
        expected_msg: str = (
            "Internal Error: Workflow instance "
            + instance_name
            + " has no version '"
            + wrong_number
            + "'."
        )

        # Act + Assert
        with self.assertRaises(InternalException) as context:
            self.w_man.set_active_version_through_number(instance_name, wrong_number)
        self.assertTrue(expected_msg in str(context.exception))

        # assert no calls to the database were made
        self.assertFalse(mock_wf_data.called)


class TestWorkflowInstanceRunning(TestWorkflowManager):
    # not an unittest - requires the server app to run
    # not automated
    # an automated integration test for this will follow
    @unittest.skip("only activate after docker-compose")
    def test_is_running(self):
        dag_ids: List[str] = [
            "example_bash_operator",
            "example_branch_datetime_operator_2",
            "example_branch_dop_operator_v3",
            "example_branch_labels",
            "example_branch_operator",
        ]
        for dag in dag_ids:
            is_running: bool = (
                self.w_man._WorkflowManager__is_workflow_instance_running(dag)
            )
            print(dag + " is running: " + str(is_running))


class TestCopyFilesWithExtension(TestWorkflowManager):
    def setUp(self):
        super(TestCopyFilesWithExtension, self).setUp()
        self.base_path_copy_whole_dir: Path = self.base_path / "copyFilesWithExtension"
        self.dst_dir: Path = self.base_path_copy_whole_dir / "dst"
        # always clear the destination directory
        if os.path.exists(self.dst_dir):
            shutil.rmtree(self.dst_dir)

    # before testing the actual method "copy_whole_dir" I want to make sure the method "are_dir_trees_equal" that is
    # used for testing works fine itself
    def test_are_dir_trees_equal_diff_dirs(self):
        # in this test I compare dirs with different tree structure
        # Arrange
        dir1: Path = self.base_path_copy_whole_dir
        dir2: Path = self.base_path_copy_whole_dir / "src3"

        # Act
        equal: bool = are_dir_trees_equal(dir1, dir2)

        # Assert
        self.assertFalse(equal)

    def test_are_dir_trees_equal_same_dir(self):
        # in this test I compare a dir to itself
        # Arrange
        dir1: Path = self.base_path_copy_whole_dir / "src3"
        dir2: Path = self.base_path_copy_whole_dir / "src3"

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

    # now we can start with the workflowtests for the actual method

    # this does not work because empty folders can't be tracked by git
    # def test_empty_dir(self):
    #     # Arrange
    #     src_path: Path = self.base_path_copy_whole_dir / "src1"
    #
    #     # Act
    #     self.w_man._WorkflowManager__copy_files_with_extension(
    #         src_path, self.dst_dir, ""
    #     )
    #
    #     # Assert
    #     self.assertTrue(are_dir_trees_equal(src_path, self.dst_dir))

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


def make_path_to_backup(base_path: Path, path: Path) -> Path:
    stack: List[str] = []
    while path != base_path:
        # remove the path after base path
        stack.append(os.path.basename(os.path.normpath(path)))
        path = path.parent
    result: Path = base_path / "backup_stuff"
    stack.reverse()
    for folder in stack:
        result = result / folder
    return result
