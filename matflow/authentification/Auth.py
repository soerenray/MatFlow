import json
from matflow.frontendapi import keys
from matflow.exceptionpackage.MatFlowException import ConverterException


class Auth:
    _basic: str

    # Constructor
    def __init__(self, auth: str):
        self._basic = auth

    @classmethod
    def extract_auth_tag(cls, json_details: str):
        """
        extracts json details and builds a new User based off of these json details

        Args:
            json_details(str): contains encoded user

        Returns:
            User: decoded user object
        """
        decoded_json: dict = json.loads(json_details)
        key_to_check = keys.auth_tag
        if key_to_check not in decoded_json:
            raise ConverterException(key_to_check + "not found")
        auth_tag: str = decoded_json[keys.auth_tag]
        auth: Auth = Auth(auth_tag)
        return auth
