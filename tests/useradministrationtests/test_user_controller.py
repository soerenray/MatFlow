import unittest
from matflow.useradministration.User import User
from matflow.useradministration.UserController import UserController
from unittest.mock import patch
from unittest.mock import call
import requests
import json
from requests.auth import HTTPBasicAuth
from matflow.exceptionpackage.MatFlowException import (
    UserExistsException,
    SignUpException,
    InternalException,
)


class MyTestCase(unittest.TestCase):
    __basic: HTTPBasicAuth

    # setUp sets up a testUser and a testUserController
    def setUp(self):
        self.testUser = User("testUsername", "inactive", "Reviewer", "testPassword")
        self.testUserController = UserController()
        self.__basic = HTTPBasicAuth("airflow", "airflow")
        requests.delete(
            "http://localhost:8080/api/v1/users/testUsername", auth=self.__basic
        )

    # tearDown deletes the testUser
    def tearDown(self):
        requests.delete(
            "http://localhost:8080/api/v1/users/testUsername", auth=self.__basic
        )

    # UserController workflowtests

    # test getAllUsersAndDetails statuscode 200 method
    def testGetAllUsersAndDetails(self):
        self.assertEqual(
            requests.get(
                "http://localhost:8080/api/v1/users",
                auth=self.__basic,
            ).json(),
            self.testUserController.getAllUsersAndDetails(self.__basic),
        )

    # test getAllUsersAndDetails statuscode != 200 method
    def testGetAllUsersAndDetails(self):
        shouldBeNone = self.testUserController.getAllUsersAndDetails(
            HTTPBasicAuth("test", "test")
        )
        shouldNotbeNone = self.testUserController.getAllUsersAndDetails(self.__basic)
        self.assertNotEqual(shouldBeNone, shouldNotbeNone)

    # test createUser
    def testCreateUserWithWrongPwRepetition(self):
        with self.assertRaises(SignUpException) as context:
            self.testUserController.createUser(
                "testUsername", "testPassword", "notTestPassword", self.__basic
            )
            self.assertTrue("Not the same Password" in context.exception)

    def testCreateUserWithAlreadyTakenUsername(self):
        with self.assertRaises(SignUpException) as context:
            self.testUserController.createUser(
                "airflow", "testPassword", "notTestPassword", self.__basic
            )
            self.assertTrue("Signup failed, User already exists" in context.exception)

    def testCreateUserCorrectly(self):
        self.testUserController.createUser(
            "testUsername", "testPassword", "testPassword", self.__basic
        )

    # test deleteUser
    def testDeleteNonexistingUser(self):
        with self.assertRaises(UserExistsException) as context:
            self.testUserController.deleteUser(self.testUser, self.__basic)
            self.assertTrue("User doesn't exist" in context.exception)

    def testDeleteUser(self):
        self.testUserController.createUser(
            "testUsername", "testPassword", "testPassword", self.__basic
        )
        self.testUserController.deleteUser(self.testUser, self.__basic)

    # test override User
    def testOverrideNonExistingUser(self):
        with self.assertRaises(UserExistsException) as context:
            self.testUserController.overrideUser(self.testUser, self.__basic)
            self.assertTrue("User doesn't exist" in context.exception)

    def testOverrideUser(self):
        self.testUserController.createUser(
            "testUsername", "testPassword", "testPassword", self.__basic
        )
        self.testUserController.overrideUser(self.testUser, self.__basic)


if __name__ == "__main__":
    unittest.main()
