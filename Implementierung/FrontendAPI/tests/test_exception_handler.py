import json
import unittest

from Implementierung.ExceptionPackage.MatFlowException import ConverterException
from Implementierung.FrontendAPI.ExceptionHandler import ExceptionHandler


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
        expected = json.loads(json.dumps({"statusCode": 611}))
        self.assertEqual(got, expected)


if __name__ == "__main__":
    unittest.main()
