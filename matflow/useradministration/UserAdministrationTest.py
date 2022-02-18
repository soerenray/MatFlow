from UserController import UserController
from User import User
import unittest
import requests
import json
from requests.auth import HTTPBasicAuth


class Tests(unittest.TestCase):

    # User tests

    # setUp sets up a testUser and a testUserController
    def setUp(self):
        self.testUser = User("testUsername", "inactive", "Reviewer", "testPassword")
        self.testUserController = UserController()

    # tearDown deletes the testUser
    # def tearDown(self):
    #    requests.delete("http://localhost:8080/api/v1/users/testUsername", auth = self.testUserController.getAuth)
    #    requests.delete("http://localhost:8080/api/v1/users/overrideUsername", auth = self.testUserController.getAuth)

    # tests the getUsername method and the User Constructor
    def testGetUsername(self):
        self.assertEqual("testUsername", self.testUser.getUsername())

    # UserController tests

    # test Authentification in the Constructor
    def testAuth(self):
        self.assertEqual(
            HTTPBasicAuth("airflow", "airflow"), self.testUserController.getAuth()
        )

    # test getAllUsersAndDetails statuscode 200 method
    def testGetAllUsersAndDetails(self):
        self.assertEqual(
            requests.get(
                "http://localhost:8080/api/v1/users",
                auth=self.testUserController.getAuth(),
            ).json(),
            self.testUserController.getAllUsersAndDetails,
        )

    # test getAllUsersAndDetails statuscode != 200 method
    def testGetAllUsersAndDetails(self):
        self.assertNotEqual(requests.get("http://localhost:8080/api/v1/users"), 200)

    # test createUser
    def testCreateUser(self):
        self.testUserController.createUser(
            "testUsername", "testPassword", "testPassword"
        )
        self.assertEqual(
            requests.get(
                "http://localhost:8080/api/v1/users/testUsername",
                auth=self.testUserController.getAuth(),
            ).status_code,
            200,
        )

    # test deleteUser
    def testDeleteUser(self):
        self.testUserController.deleteUser(self.testUser)
        self.assertNotEqual(
            requests.get(
                "http://localhost:8080/api/v1/users/testUsername",
                auth=self.testUserController.getAuth(),
            ).status_code,
            200,
        )

    # test check Usernames
    def testCheckUsernames(self):
        overrideTestUser = User("testUsername", "active", "Viewer", "overridePassword")
        self.testUserController.createUser(
            "testUsername", "testPassword", "testPassword"
        )
        self.assertEqual(
            requests.get(
                "http://localhost:8080/api/v1/users/testUsername",
                auth=self.testUserController.getAuth(),
            ).json()["roles"][0]["name"],
            "Public",
        )
        self.testUserController.overrideUser(overrideTestUser)
        print(self.testUserController.overrideUser(overrideTestUser))
        self.assertEqual(
            requests.get(
                "http://localhost:8080/api/v1/users/testUsername",
                auth=self.testUserController.getAuth(),
            ).json()["roles"][0]["name"],
            "Viewer",
        )
        self.testUserController.deleteUser(overrideTestUser)

    # to be tested:

    # # test login User
    # def testLoginUser(self):
    #     self.testUserController.createUser("testUsername","testPassword","testPassword")
    #     self.testUserController.loginUser("testUsername","testPassword")
    #     self.testUserController.deleteUser(self.testUser)

    # test Exceptions


if __name__ == "__main__":
    unittest.main()
