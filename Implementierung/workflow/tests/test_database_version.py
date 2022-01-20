from unittest import TestCase
from pathlib import Path
from workflow.database_version import DatabaseVersion
from workflow.version_number import VersionNumber
from workflow.parameter_change import ParameterChange


class TestDatabaseVersion(TestCase):
    def setUp(self):
        self.base_path = "test_files/database_version/"
        configs_dir1 = Path(self.base_path + "changed_files")
        version_number = VersionNumber("1.1")
        self.version1 = DatabaseVersion(version_number, "", configs_dir1)


class TestGetFrontendVersion(TestDatabaseVersion):

    def test_too_little_files(self):
        # there are too little files to compare

        # Arrange
        comparison_files = Path(self.base_path + "too_little_files")
        expected_msg = \
            "Internal Error: Too little comparison files for version " + self.version1.get_version_number().get_number()

        # Act + Assert
        with self.assertRaises(Exception) as context:
            self.version1.get_frontend_version(comparison_files)
        self.assertTrue(expected_msg in str(context.exception))

    def test_too_many_files(self):
        # there are too many files to compare

        # Arrange
        comparison_files = Path(self.base_path + "too_many_files")
        expected_msg = \
            "Internal Error: Too many comparison files for version " + self.version1.get_version_number().get_number()

        # Act + Assert
        with self.assertRaises(Exception) as context:
            self.version1.get_frontend_version(comparison_files)
        self.assertTrue(expected_msg in str(context.exception))

    def test_wrong_files(self):
        # the names of the comparison files don't match

        # Arrange
        comparison_files = Path(self.base_path + "wrong_files")
        expected_msg = \
            "Internal Error: Wrong comparison files for version " + self.version1.get_version_number().get_number()

        # Act + Assert
        with self.assertRaises(Exception) as context:
            self.version1.get_frontend_version(comparison_files)
        self.assertTrue(expected_msg in str(context.exception))

    def test_valid_files(self):
        # the case in witch there are valid comparison files

        # Arrange
        comparison_files = Path(self.base_path + "previous_files")

        # Act
        expected = [ParameterChange("key3", "i_was", "value3", "changed", "test1.conf"),
                    ParameterChange("key5", "key55", "value5", "value5", "test2.conf"),
                    ParameterChange("key6", "key6", "value6", "6", "test2.conf")]
        frontend_version = self.version1.get_frontend_version(comparison_files)
        actual = frontend_version.get_changes()

        # Assert
        # TODO comparing ParameterChanges doesn't work
        self.assertEqual(expected, actual)
