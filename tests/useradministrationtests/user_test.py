import json
import unittest

# TODO User test cases encoding/decoding
from copy import deepcopy
from unittest.mock import patch

from matflow.exceptionpackage.MatFlowException import ConverterException
from matflow.frontendapi import keys
from matflow.useradministration.User import User


class UserTest(unittest.TestCase):
    def setUp(self) -> None:
        self.user: User = User("scooby", "active", "reviewer", "scooby_snacks")
        self.expected_encoding = {
            keys.user_name: "scooby",
            keys.user_status_name: "active",
            keys.user_privilege_name: "reviewer",
        }
        self.expected_extracting = deepcopy(self.expected_encoding)
        self.expected_extracting.update({keys.password_name: "scooby_snacks"})

    # only valid encoding possible
    def test_encode_valid(self):
        self.assertEqual(self.user.encode_user(), self.expected_encoding)

    def test_encode_call_name(self):
        with patch.object(User, "getUsername", return_value="") as mock_method:
            self.user.encode_user()
            assert mock_method.call_count > 0

    def test_encode_call_status(self):
        with patch.object(User, "getStatus", return_value="") as mock_method:
            self.user.encode_user()
            assert mock_method.call_count > 0

    def test_encode_call_privilege(self):
        with patch.object(User, "getPrivilege", return_value="") as mock_method:
            self.user.encode_user()
            assert mock_method.call_count > 0

    def test_extract_user_valid(self):
        extracted = User.extract_user(json.dumps(self.expected_extracting))
        self.assertEqual(extracted.getStatus(), self.user.getStatus())
        self.assertEqual(extracted.getUsername(), self.user.getUsername())
        self.assertEqual(extracted.getPrivilege(), self.user.getPrivilege())
        self.assertEqual(extracted.getPassword(), self.user.getPassword())

    def test_extract_user_fail_status(self):
        to_dump = deepcopy(self.expected_extracting)
        to_dump.pop(keys.user_status_name)
        with self.assertRaises(ConverterException):
            User.extract_user(json.dumps(to_dump))

    def test_extract_user_fail_privilege(self):
        to_dump = deepcopy(self.expected_extracting)
        to_dump.pop(keys.user_privilege_name)
        with self.assertRaises(ConverterException):
            User.extract_user(json.dumps(to_dump))

    def test_extract_user_fail_name(self):
        to_dump = deepcopy(self.expected_extracting)
        to_dump.pop(keys.user_name)
        with self.assertRaises(ConverterException):
            User.extract_user(json.dumps(to_dump))

    def test_extract_user_fail_password(self):
        to_dump = deepcopy(self.expected_extracting)
        to_dump.pop(keys.password_name)
        with self.assertRaises(ConverterException):
            User.extract_user(json.dumps(to_dump))


if __name__ == "__main__":
    unittest.main()
