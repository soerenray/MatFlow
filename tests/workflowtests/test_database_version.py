from typing import List, Tuple
from unittest import TestCase
from pathlib import Path
from matflow.workflow.database_version import DatabaseVersion
from matflow.workflow.frontend_version import FrontendVersion
from matflow.workflow.version_number import VersionNumber
from matflow.workflow.parameter_change import ParameterChange
from matflow.exceptionpackage.MatFlowException import InternalException


class TestDatabaseVersion(TestCase):
    def setUp(self):
        self.base_path: Path = (
            Path(__file__).parent.absolute() / "test_files/database_version/"
        )
        configs_dir1: Path = self.base_path / "changed_files"
        version_number: VersionNumber = VersionNumber("1.1")
        self.version1: DatabaseVersion = DatabaseVersion(
            version_number, "", configs_dir1
        )


class ParameterChangeMatcher:
    # class for comparing lists of ParameterChange objects
    expected: List[ParameterChange]

    def __init__(self, expected):
        self.expected = expected

    def __eq__(self, other: List[ParameterChange]):
        if len(self.expected) != len(other):
            return False
        else:
            for exp, act in zip(self.expected, other):
                if not (
                    exp.get_old_key() == act.get_old_key()
                    and exp.get_new_key() == act.get_new_key()
                    and exp.get_old_value() == act.get_old_value()
                    and exp.get_new_value() == act.get_new_value()
                    and exp.get_config_file_name() == act.get_config_file_name()
                ):
                    return False
            return True


class TestGetFrontendVersion(TestDatabaseVersion):
    def test_too_little_files(self):
        # there are too little files to compare

        # Arrange
        comparison_names: List[str] = ["test2.conf"]
        comparison_paths: List[Path] = [self.base_path / "too_many_files/test2.conf"]
        comparison_files: List[Tuple[str, Path]] = list(
            zip(comparison_names, comparison_paths)
        )
        expected_msg: str = (
            "Internal Error: Too little comparison files for version "
            + self.version1.get_version_number().get_number()
        )

        # Act + Assert
        with self.assertRaises(InternalException) as context:
            self.version1.get_frontend_version(comparison_files)
        self.assertTrue(expected_msg in str(context.exception))

    def test_too_many_files(self):
        # there are too many files to compare

        # Arrange
        comparison_names: List[str] = ["test1.conf", "test2.conf", "test3.conf"]
        comparison_paths: List[Path] = [
            self.base_path / "too_many_files/test1.conf",
            self.base_path / "too_many_files/test2.conf",
            self.base_path / "too_many_files/test3.conf",
        ]
        comparison_files: List[Tuple[str, Path]] = list(
            zip(comparison_names, comparison_paths)
        )
        expected_msg: str = (
            "Internal Error: Too many comparison files for version "
            + self.version1.get_version_number().get_number()
        )

        # Act + Assert
        with self.assertRaises(InternalException) as context:
            self.version1.get_frontend_version(comparison_files)
        self.assertTrue(expected_msg in str(context.exception))

    def test_wrong_files(self):
        # the names of the comparison files don't match

        # Arrange
        comparison_names: List[str] = ["test1.conf", "test3.conf"]
        comparison_paths: List[Path] = [
            self.base_path / "wrong_files/test1.conf",
            self.base_path / "wrong_files/test3.conf",
        ]
        comparison_files: List[Tuple[str, Path]] = list(
            zip(comparison_names, comparison_paths)
        )
        expected_msg: str = (
            "Internal Error: Wrong comparison files for version "
            + self.version1.get_version_number().get_number()
        )

        # Act + Assert
        with self.assertRaises(InternalException) as context:
            self.version1.get_frontend_version(comparison_files)
        self.assertTrue(expected_msg in str(context.exception))

    def test_valid_files(self):
        # the case in witch there are valid comparison files

        # Arrange
        comparison_names: List[str] = ["test1.conf", "test2.conf"]
        comparison_paths: List[Path] = [
            self.base_path / "previous_files/test1.conf",
            self.base_path / "previous_files/test2.conf",
        ]
        comparison_files: List[Tuple[str, Path]] = list(
            zip(comparison_names, comparison_paths)
        )

        # Act
        expected: List[ParameterChange] = [
            ParameterChange("key3", "i_was", "value3", "changed", "test1.conf"),
            ParameterChange("key5", "key55", "value5", "value5", "test2.conf"),
            ParameterChange("key6", "key6", "value6", "6", "test2.conf"),
        ]
        frontend_version: FrontendVersion = self.version1.get_frontend_version(
            comparison_files
        )
        actual: List[ParameterChange] = frontend_version.get_changes()

        # Assert
        self.assertEqual(ParameterChangeMatcher(expected), actual)
