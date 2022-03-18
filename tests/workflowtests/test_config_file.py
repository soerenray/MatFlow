from typing import TextIO, List, Tuple
from unittest import TestCase
from pathlib import Path
from matflow.workflow.config_file import ConfigFile
from matflow.workflow.reduced_config_file import ReducedConfigFile
from matflow.exceptionpackage.MatFlowException import InternalException


class TestConfigFile(TestCase):
    path1: Path
    config1: ConfigFile
    path1_updated: Path
    config1_update: ReducedConfigFile
    back_up_path: Path
    config1_contend: str

    def setUp(self):
        # set up paths and config-file objects

        self.base_path: Path = Path(__file__).parent.absolute() / "test_files/config_file"
        self.path1 = self.base_path / "test1.conf"
        self.config1 = ConfigFile("test1", self.path1)
        self.path1_updated = self.base_path / "test1updated.conf"
        self.config1_update = ReducedConfigFile(
            "test1",
            [
                ("i_was", "replaced"),
                ("this_one", "as_well"),
                ("four", "4"),
                ("also", "find_me"),
            ],
        )

        # prepare the contents of the backup file
        self.back_up_path = self.base_path / "test1backUp.conf"
        backup_file1: TextIO = open(self.back_up_path)
        self.config1_contend = backup_file1.read()
        backup_file1.close()

    def tearDown(self):
        # restore the content of test1
        file1: TextIO = open(self.config1.get_file(), "w")
        file1.write(self.config1_contend)
        file1.close()


class TestInit(TestConfigFile):
    def test_not_none(self):
        self.assertIsNotNone(self.config1)

    def test_name(self):
        expected: str = "test1"
        actual: str = self.config1.get_file_name()
        self.assertEqual(expected, actual)

    def test_key_value_pairs(self):
        # this is actually a test for the __extract_key_value_pairs_from_file method that is used in the constructor
        expected: List[Tuple[str, str]] = [
            ("find", "this_pair"),
            ("this_one", "as_well"),
            ("three", "3"),
            ("also", "find_me"),
        ]
        actual: List[Tuple[str, str]] = self.config1.get_key_value_pairs()
        self.assertEqual(expected, actual)


class TestFindChanges(TestConfigFile):
    def test_len_not_equal(self):
        # pair-lists of different lengths should not be comparable

        expected_msg: str = (
            "Internal Error: Wrong amount of update-pairs in "
            + self.config1.get_file_name()
        )

        to_little_pairs: ReducedConfigFile = ReducedConfigFile(
            "toShort", [("key", "value")]
        )
        with self.assertRaises(InternalException) as context:
            self.config1.find_changes(to_little_pairs)
        self.assertTrue(expected_msg in str(context.exception))

        to_many_pairs: ReducedConfigFile = ReducedConfigFile(
            "toShort",
            [
                ("key", "value"),
                ("key", "value"),
                ("key", "value"),
                ("key", "value"),
                ("key", "value"),
            ],
        )
        with self.assertRaises(InternalException) as context:
            self.config1.find_changes(to_many_pairs)
        self.assertTrue(expected_msg in str(context.exception))

    def test_no_changes(self):
        # we expect an empty list
        self.assertFalse(self.config1.find_changes(self.config1))

    def test_valid_changes(self):
        expected: List[Tuple[str, str, str, str]] = [
            ("find", "i_was", "this_pair", "replaced"),
            ("three", "four", "3", "4"),
        ]
        actual: List[Tuple[str, str, str, str]] = self.config1.find_changes(
            self.config1_update
        )
        self.assertEqual(expected, actual)


class TestWriteChangesToFile(TestConfigFile):
    def test_pair_not_in_file(self):
        missing_pair: Tuple[str, str] = ("i'm", "missing")
        expected_msg: str = (
            "Internal Error: Pair: "
            + str(missing_pair)
            + "doesn't occur in file: "
            + self.config1.get_file_name()
        )

        missing_pair_update = [("i'm", "new_key", "missing", "new_value")]
        with self.assertRaises(InternalException) as context:
            self.config1._ConfigFile__write_changes_to_file(missing_pair_update)
        self.assertTrue(expected_msg in str(context.exception))

    def test_no_changes(self):
        self.config1._ConfigFile__write_changes_to_file([])  # update list empty

        expected: str = self.config1_contend

        actual_file: TextIO = open(self.config1.get_file())
        actual: str = actual_file.read()
        actual_file.close()

        self.assertEqual(
            expected, actual
        )  # the test file isn't too big, so we can compare the strings

    def test_valid_changes(self):
        changes: object = self.config1.find_changes(
            self.config1_update
        )  # we tested this method above
        self.config1._ConfigFile__write_changes_to_file(changes)  # update list empty

        expected_file: TextIO = open(self.path1_updated)
        expected: str = expected_file.read()
        expected_file.close()

        actual_file: TextIO = open(self.config1.get_file())
        actual: str = actual_file.read()
        actual_file.close()

        self.assertEqual(expected, actual)


class ApplyChanges(TestConfigFile):
    def test_no_changes(self):
        self.config1.apply_changes(self.config1)
        # there are no changes so the file should be unchanged

        expected = self.config1_contend

        actual_file: TextIO = open(self.config1.get_file())
        actual: str = actual_file.read()
        actual_file.close()

        self.assertEqual(expected, actual)

    def test_update_wrong_name(self):
        # the ReducedConfigFile that represents the update should definitely have the same name as the present file
        wrong_name: ConfigFile = ConfigFile("wrong_name", self.path1_updated)
        expected_msg: str = (
            "Internal Error: Names of the file: "
            + self.config1.get_file_name()
            + " and the update: "
            + wrong_name.get_file_name()
            + " don't match."
        )
        with self.assertRaises(InternalException) as context:
            self.config1.apply_changes(wrong_name)
        self.assertTrue(expected_msg in str(context.exception))

    def test_valid_changes(self):
        self.config1.apply_changes(self.config1_update)

        expected_file: TextIO = open(self.path1_updated)
        expected: str = expected_file.read()
        expected_file.close()

        actual_file: TextIO = open(self.config1.get_file())
        actual: str = actual_file.read()
        actual_file.close()

        self.assertEqual(expected, actual)
