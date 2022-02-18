import unittest
from pathlib import Path
from unittest.mock import patch, mock_open

from matflow.frontendapi import utilities


class UtilitiesTest(unittest.TestCase):
    def test_create_dir_valid(self):
        expected = "scooby_0"
        with patch.object(utilities.os.path, "isdir", return_value=False):
            with patch.object(utilities.os, "makedirs"):
                got = utilities.create_dir("scooby")
                self.assertEqual(got, expected)

    def test_create_dir_invalid(self):
        expected = "scooby_1"
        with patch.object(utilities.os.path, "isdir", return_value=False):
            with patch.object(utilities.os, "makedirs"):
                got = utilities.create_dir("scooby")
                self.assertNotEqual(got, expected)

    def test_create_dir_call_isdir(self):
        expected = "scooby_1"
        with patch.object(
            utilities.os.path, "isdir", return_value=False
        ) as mock_method:
            with patch.object(utilities.os, "makedirs"):
                got = utilities.create_dir("scooby")
                assert mock_method.call_count > 0

    def test_create_dir_call_makedirs(self):
        expected = "scooby_1"
        with patch.object(utilities.os.path, "isdir", return_value=False):
            with patch.object(utilities.os, "makedirs") as mock_method:
                got = utilities.create_dir("scooby")
                assert mock_method.call_count > 0

    def test_encode_file_valid(self):
        with patch("builtins.open", mock_open(read_data="data")):
            with patch.object(utilities, "b64encode", return_value="scooby"):
                with patch.object(utilities.os, "remove"):
                    got = utilities.encode_file(Path("/path"), "key_scooby")
                    self.assertEqual({"key_scooby": "scooby"}, got)

    def test_encode_file_invalid(self):
        with patch("builtins.open", mock_open(read_data="data")):
            with patch.object(utilities, "b64encode", return_value="scooby"):
                with patch.object(utilities.os, "remove"):
                    got = utilities.encode_file(Path("/path"), "key_scooby")
                    self.assertNotEqual({"key_scooby": ""}, got)

    def test_encode_file_call_open(self):
        with patch("builtins.open", mock_open(read_data="data")) as mock_method:
            with patch.object(utilities, "b64encode", return_value="scooby"):
                with patch.object(utilities.os, "remove"):
                    got = utilities.encode_file(Path("/path"), "key_scooby")
                    assert mock_method.call_count > 0

    def test_encode_file_call_encode(self):
        with patch("builtins.open", mock_open(read_data="data")):
            with patch.object(
                utilities, "b64encode", return_value="scooby"
            ) as mock_method:
                with patch.object(utilities.os, "remove"):
                    got = utilities.encode_file(Path("/path"), "key_scooby")
                    assert mock_method.call_count > 0

    def test_encode_file_call_remove(self):
        with patch("builtins.open", mock_open(read_data="data")):
            with patch.object(utilities, "b64encode", return_value="scooby"):
                with patch.object(utilities.os, "remove") as mock_method:
                    got = utilities.encode_file(Path("/path"), "key_scooby")
                    assert mock_method.call_count > 0

    def test_decode_file_valid(self):
        with patch.object(utilities, "b64decode", return_value="scooby"):
            self.assertEqual(utilities.decode_file("bczcbechec"), "scooby")

    def test_decode_file_call(self):
        with patch.object(utilities, "b64decode", return_value="scooby") as mock_method:
            utilities.decode_file("jbch")
            assert mock_method.call_count > 0


if __name__ == "__main__":
    unittest.main()
