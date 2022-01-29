from __future__ import annotations

from typing import List

from flask import request
# User class
#
# username: the Users Username
# status: the Users status (is either "active" or "inactive") 
# privilege: the Users privilege, no privilege equals inactive status 
# password: the Users password
from Implementierung.FrontendAPI import keys
from Implementierung.FrontendAPI.ExceptionHandler import ExceptionHandler


class User:
    _username: str
    _status: str
    _privilege: str
    _password: str

    # Construktor
    def __init__(self, username: str, status: str, privilege: str, password: str):
        self._username = username
        self._status = status
        self._privilege = privilege
        self._password = password

    # getter and setter methods:

    # username getter method
    def getUsername(self):
        return self._username

    # username setter method
    def setUsername(self, username):
        self._username = username

    # status getter method
    def getStatus(self):
        return self._status

    # status setter method
    def setStatus(self, status):
        self._status = status

    # privilege getter method
    def getPrivilege(self):
        return self._privilege

    # privilege setter method
    def setPrivilege(self, priv):
        self._privilege = priv

    # password getter method
    def getPassword(self):
        return self._password

    # password setter method
    def setPrivilege(self, password):
        self._password = password

    @classmethod
    def extract_user(cls, request_details: request) -> User:
        """
        extracts json details and builds a new User based off of these json details

        Args:
            request_details(request): contains encoded user

        Returns:
            User: decoded user object
        """
        user_name: str = request_details.args.get(keys.user_name)
        status: str = request_details.args.get(keys.user_status_name)
        privilege: str = request_details.args.get(keys.user_privilege_name)
        password: str = request_details.args.get(keys.password_name)
        user: User = User(user_name, status, privilege, password)
        return user

    def encode_user(self) -> dict:
        """
        encodes all user attributes and dumps them into json object

        Returns:
            String: json-dumped object containing encoded user
        """

        out_dict: dict = dict()
        out_dict.update({keys.user_name: self.getUsername(), keys.user_status_name: self.getStatus(),
                         keys.user_privilege_name: self.getPrivilege()})
        return out_dict
