import json
import unittest

from matflow.exceptionpackage.MatFlowException import ConverterException
from matflow.frontendapi.ExceptionHandler import ExceptionHandler


class ExceptionHandlerTest(unittest.TestCase):
    def test_send_status_code(self):
        got = ExceptionHandler.send_status_code(607, {})
        self.assertEqual(got, {"statusCode": 607})

    def test_send_success(self):
        got = json.loads(ExceptionHandler.success({}))
        expected = json.loads(json.dumps({"statusCode": 607}))
        self.assertEqual(got, expected)

    def test_handle_exception(self):
        got = json.loads(
            ExceptionHandler.handle_exception(ConverterException("whoops"))
        )
        expected = json.loads(
            json.dumps({"statusCode": 611, "error_message": "whoops"})
        )
        self.assertEqual(got, expected)


if __name__ == "__main__":
    unittest.main()
