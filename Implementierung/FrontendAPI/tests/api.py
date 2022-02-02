import unittest
import json
from Implementierung.FrontendAPI.api import app

"""
Entry module for tests. Disclaimer: InternalException is used as a placeholder for dev purposes. It is only important
to have an exception raised, not which one exactly.
The point of these unit tests is to prove that the small functions work, i.e. all calls are made and the 
json is in the right format. That's why the posted json does not have to be called with the right keys, that is
part of the integration test.
"""


def create_json(dictionary: dict) -> str:
    return json.dumps(dictionary)


success_response: dict = {"statusCode": 607}


class APITest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()

    def test_api_reachability(self):
        posted = self.app.post('/')
        retrieved_json: dict = json.loads(posted.get_data())
        self.assertEqual(success_response, retrieved_json)


if __name__ == '__main__':
    unittest.main()
