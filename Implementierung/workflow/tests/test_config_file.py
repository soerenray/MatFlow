from unittest import TestCase
from pathlib import Path
from workflow.config_file import ConfigFile


class TestConfigFile(TestCase):
    def setUp(self):
        self.path1 = Path("test_files/test1.conf")
        self.config1 = ConfigFile("test1", self.path1)


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
