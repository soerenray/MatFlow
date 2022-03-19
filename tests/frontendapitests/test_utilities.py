import base64
import builtins
import os.path
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from matflow.frontendapi import utilities


class UtilitiesTest(unittest.TestCase):
    def setUp(self) -> None:
        res_path = os.path.join(Path(__file__).parent, "res")
        self.file_path = Path(os.path.join(res_path, "gibberish.py"))
        self.mock_open = MagicMock()

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
        with patch.object(
            utilities, "b64encode", return_value="scooby".encode("utf-8")
        ):
            with patch.object(utilities.os, "remove"):
                got = utilities.encode_file(self.file_path, "key_scooby", True)
                self.assertEqual({"key_scooby": "scooby"}, got)

    def test_encode_file_invalid(self):
        with patch.object(
            utilities, "b64encode", return_value="scooby".encode("utf-8")
        ):
            with patch.object(utilities.os, "remove"):
                got = utilities.encode_file(self.file_path, "key_scooby", True)
                self.assertNotEqual({"key_scooby": "schooooby"}, got)

    def test_encode_file_call_encode(self):
        with patch.object(
            utilities, "b64encode", return_value="scooby".encode("utf-8")
        ) as mock_method:
            with patch.object(utilities.os, "remove"):
                got = utilities.encode_file(self.file_path, "key_scooby", True)
                assert mock_method.call_count > 0

    def test_encode_file_call_remove(self):
        with patch.object(
            utilities, "b64encode", return_value="scooby".encode("utf-8")
        ):
            with patch.object(utilities.os, "remove") as mock_method:
                got = utilities.encode_file(self.file_path, "key_scooby", True)
                assert mock_method.call_count > 0

    def test_encode_file_call_write(self):
        with patch.object(
            utilities, "b64encode", return_value="scooby".encode("utf-8")
        ):
            with patch.object(utilities.os, "remove"):
                with patch.object(
                    builtins, "open", return_value=self.mock_open
                ) as mock_method:
                    got = utilities.encode_file(self.file_path, "key_scooby", True)
                    assert mock_method.call_count > 0

    def test_decode_file_valid(self):
        # implicitly calls tested as well due to encoding/decoding/file writing
        res_path = os.path.join(Path(__file__).parent, "res")
        file_path = os.path.join(res_path, "gibberish.py")
        file_path_2 = os.path.join(res_path, "gibberish2.py")
        # encode file gibberish.py
        with open(file_path, "r") as file:
            encoding = base64.b64encode(file.read().encode("utf-8")).decode("utf-8")
        # encoding is: b'aGVsbG8gPSAid29ybGQi'
        utilities.decode_file(encoding, file_path_2)
        with open(file_path, "r") as file:
            self.assertEqual(
                base64.b64encode(file.read().encode("utf-8")).decode("utf-8"), encoding
            )
        os.remove(file_path_2)


if __name__ == "__main__":
    unittest.main()
