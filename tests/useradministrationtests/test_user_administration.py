from matflow.useradministration.UserController import UserController
from matflow.useradministration.User import User
import unittest
import requests
import json
from requests.auth import HTTPBasicAuth


class Tests(unittest.TestCase):

    # User workflowtests

    # setUp sets up a testUser and a testUserController
    def setUp(self):
        self.testUser = User("testUsername", "inactive", "Reviewer", "testPassword")
        self.testUserController = UserController()

    # tearDown deletes the testUser
    # def tearDown(self):
    #    requests.delete("http://localhost:8080/api/v1/users/testUsername", auth = self.testUserController.getAuth)
    #    requests.delete("http://localhost:8080/api/v1/users/overrideUsername", auth = self.testUserController.getAuth)

    # workflowtests the getUsername method and the User Constructor
    @unittest.skip("Airflow needs to be up")
    def testGetUsername(self):
        self.assertEqual("testUsername", self.testUser.getUsername())

    # UserController workflowtests

    # test Authentification in the Constructor
    @unittest.skip("Airflow needs to be up")
    def testAuth(self):
        self.assertEqual(
            HTTPBasicAuth("airflow", "airflow"), self.testUserController.getAuth()
        )

    # test getAllUsersAndDetails statuscode 200 method
    @unittest.skip("Airflow needs to be up")
    def testGetAllUsersAndDetails(self):
        self.assertEqual(
            requests.get(
                "http://localhost:8080/api/v1/users",
                auth=self.testUserController.getAuth(),
            ).json(),
            self.testUserController.getAllUsersAndDetails,
        )

    # test getAllUsersAndDetails statuscode != 200 method
    @unittest.skip("Airflow needs to be up")
    def testGetAllUsersAndDetails(self):
        self.assertNotEqual(requests.get("http://localhost:8080/api/v1/users"), 200)

    # test createUser
    @unittest.skip("Airflow needs to be up")
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
    @unittest.skip("Airflow needs to be up")
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
    @unittest.skip("Airflow needs to be up")
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
