from typing import List
from unittest import TestCase
from workflow.version_number import VersionNumber
from ExceptionPackage.MatFlowException import InternalException


class TestVersionNumber(TestCase):
    def test_constructor(self):
        valid_numbers: List[str] = ["1.1.1.1", "1", "1.2.3.4.5", "1.3.44.15"]
        invalid_numbers: List[str] = ["", "1.a.1", "2.1.1", "abc", "1.2.1."]

        for number in valid_numbers:
            version_number: VersionNumber = VersionNumber(number)
            self.assertEqual(version_number.get_number(), number)

        for number in invalid_numbers:
            expected_msg: str = "Internal Error: " + number + " isn't a valid version number."
            with self.assertRaises(InternalException) as context:
                VersionNumber(number)
            self.assertTrue(expected_msg in str(context.exception))

    def test_valid_get_predecessor(self):
        # Arrange
        versions: List[str] = ["1.1.1.1", "1.2.3.4.5", "1.3.44.15"]
        expected: List[str] = ["1.1.1", "1.2.3.4", "1.3.44"]

        # Act
        actual = []
        for number in versions:
            vn: VersionNumber = VersionNumber(number)
            actual.append(vn.get_predecessor().get_number())

        # Assert
        self.assertEqual(expected, actual)

    def test_get_predecessor_of_1(self):
        # Arrange
        vn: VersionNumber = VersionNumber("1")
        expected_msg: str = "Internal Error: Version '1' has no predecessor."

        # Act + Assert
        with self.assertRaises(InternalException) as context:
            vn.get_predecessor()
        self.assertTrue(expected_msg in str(context.exception))


class TestGetSuccessor(TestVersionNumber):
    def test_get_successor_with_no_other_versions(self):
        # Arrange
        versions: List[str] = []
        current_version: VersionNumber = VersionNumber("1.1")
        expected: str = "1.1.1"

        # Act
        successor: VersionNumber = current_version.get_successor(versions)
        actual: str = successor.get_number()

        # Assert
        self.assertEqual(expected, actual)

    def test_get_successor_with_other_versions(self):
        # Arrange
        versions: List[str] = ["1", "1.1", "1.1.1", "1.1.2"]
        current_version: VersionNumber = VersionNumber("1.1")
        expected: str = "1.1.3"

        # Act
        successor: VersionNumber = current_version.get_successor(versions)
        actual: str = successor.get_number()

        # Assert
        self.assertEqual(expected, actual)
