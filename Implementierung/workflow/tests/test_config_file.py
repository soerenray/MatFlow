from unittest import TestCase
from pathlib import Path
from workflow.config_file import ConfigFile
from workflow.reduced_config_file import ReducedConfigFile


class TestConfigFile(TestCase):
    def setUp(self):
        # set up paths and config-file objects

        self.path1 = Path("test_files/config_file/test1.conf")
        self.config1 = ConfigFile("test1", self.path1)
        self.path1_updated = Path("test_files/config_file/test1updated.conf")
        self.config1_update = ReducedConfigFile(
            "test1", [("i_was", "replaced"), ("this_one", "as_well"), ("four", "4"), ("also", "find_me")])

        # restore the content of test1

        self.back_up_path = Path("test_files/config_file/test1backUp.conf")
        backup_file1 = open(self.back_up_path)
        self.config1_contend = backup_file1.read()
        backup_file1.close()

        file1 = open(self.config1.get_file(), "w")
        file1.write(self.config1_contend)
        file1.close()


class TestInit(TestConfigFile):
    def test_not_none(self):
        self.assertIsNotNone(self.config1)

    def test_name(self):
        expected = "test1"
        actual = self.config1.get_file_name()
        self.assertEqual(expected, actual)

    def test_key_value_pairs(self):
        # this is actually a test for the __extract_key_value_pairs_from_file method that is used in the constructor
        expected = [("find", "this_pair"), ("this_one", "as_well"), ("three", "3"), ("also", "find_me")]
        actual = self.config1.get_key_value_pairs()
        self.assertEqual(expected, actual)


class TestFindChanges(TestConfigFile):
    def test_len_not_equal(self):
        # pair-lists of different lengths should not be comparable

        expected_msg = "Internal Error: Wrong amount of update-pairs in " + self.config1.get_file_name()

        to_little_pairs = ReducedConfigFile("toShort", [("key", "value")])
        with self.assertRaises(Exception) as context:
            self.config1.find_changes(to_little_pairs)
        self.assertTrue(expected_msg in str(context.exception))

        to_many_pairs = ReducedConfigFile(
            "toShort", [("key", "value"), ("key", "value"), ("key", "value"), ("key", "value"), ("key", "value")])
        with self.assertRaises(Exception) as context:
            self.config1.find_changes(to_many_pairs)
        self.assertTrue(expected_msg in str(context.exception))

    def test_no_changes(self):
        # we expect an empty list
        self.assertFalse(self.config1.find_changes(self.config1))

    def test_valid_changes(self):
        expected = [("find", "i_was", "this_pair", "replaced"), ("three", "four", "3", "4")]
        actual = self.config1.find_changes(self.config1_update)
        self.assertEqual(expected, actual)


class TestWriteChangesToFile(TestConfigFile):
    def test_pair_not_in_file(self):
        missing_pair = ("i'm", "missing")
        expected_msg = \
            "Internal Error: Pair: " + str(missing_pair) + "doesn't occur in file: " + self.config1.get_file_name()

        missing_pair_update = [("i'm", "new_key", "missing", "new_value")]
        with self.assertRaises(Exception) as context:
            self.config1._ConfigFile__write_changes_to_file(missing_pair_update)
        self.assertTrue(expected_msg in str(context.exception))

    def test_no_changes(self):
        self.config1._ConfigFile__write_changes_to_file([])  # update list empty

        expected = self.config1_contend

        actual_file = open(self.config1.get_file())
        actual = actual_file.read()
        actual_file.close()

        self.assertEqual(expected, actual)  # the test file isn't too big, so we can compare the strings

    def test_valid_changes(self):
        changes = self.config1._ConfigFile__find_changes(self.config1_update)  # we tested this method above
        self.config1._ConfigFile__write_changes_to_file(changes)  # update list empty

        expected_file = open(self.path1_updated)
        expected = expected_file.read()
        expected_file.close()

        actual_file = open(self.config1.get_file())
        actual = actual_file.read()
        actual_file.close()

        self.assertEqual(expected, actual)


class ApplyChanges(TestConfigFile):
    def test_no_changes(self):
        self.config1.apply_changes(self.config1)
        # there are no changes so the file should be unchanged

        expected = self.config1_contend

        actual_file = open(self.config1.get_file())
        actual = actual_file.read()
        actual_file.close()

        self.assertEqual(expected, actual)

    def test_update_wrong_name(self):
        # the ReducedConfigFile that represents the update should definitely have the same name as the present file
        wrong_name = ConfigFile("wrong_name", self.path1_updated)
        expected_msg = "Internal Error: Names of the file: " + self.config1.get_file_name() + \
                       " and the update: " + wrong_name.get_file_name() + " don't match."
        with self.assertRaises(Exception) as context:
            self.config1.apply_changes(wrong_name)
        self.assertTrue(expected_msg in str(context.exception))

    def test_valid_changes(self):
        self.config1.apply_changes(self.config1_update)

        expected_file = open(self.path1_updated)
        expected = expected_file.read()
        expected_file.close()

        actual_file = open(self.config1.get_file())
        actual = actual_file.read()
        actual_file.close()

        self.assertEqual(expected, actual)
