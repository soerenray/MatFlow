from unittest import TestCase
from workflow.version_number import VersionNumber


class TestVersionNumber(TestCase):
    def test_constructor(self):
        valid_numbers = ["1.1.1.1", "1", "1.2.3.4.5", "1.3.44.15"]
        invalid_numbers = ["", "1.a.1", "2.1.1", "abc", "1.2.1."]

        for number in valid_numbers:
            version_number = VersionNumber(number)
            self.assertEqual(version_number.get_number(), number)

        for number in invalid_numbers:
            expected_msg = "Internal Error: " + number + " isn't a valid version number."
            with self.assertRaises(Exception) as context:
                VersionNumber(number)
            self.assertTrue(expected_msg in str(context.exception))



