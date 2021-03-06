from matflow.frontendapi import keys
from matflow.useradministration.User import User
from requests.auth import HTTPBasicAuth
import requests
from matflow.exceptionpackage.MatFlowException import (
    UserExistsException,
    SignUpException,
    InternalException,
)


class UserController:

    # CONSTRUCTOR
    #
    def __init__(self):
        pass

    # METHODS

    # getAllUsersAndDetails method:
    #
    # this method uses the Airflow Rest API to return all the users and their details listed in the database
    #
    # "listUsers" is the response from the API call
    #
    # the return of this method should look like this:
    #     {
    #       "users": [
    #                 {
    #                   "active": true,
    #                   "changed_on": "string",
    #                   "created_on": "string",
    #                   "email": "string",
    #                   "failed_login_count": 0,
    #                   "first_name": "string",
    #                   "last_login": "string",
    #                   "last_name": "string",
    #                   "login_count": 0,
    #                   "roles": [
    #                               {
    #                                   "name": "string"
    #                               }
    #                            ],
    #                   "username": "string"
    #                  }
    #                 ],
    #      "total_entries": 0
    #    }

    def getAllUsersAndDetails(self, basic: (str, str)):
        listUsers = requests.get(keys.airflow_address + "api/v1/users", auth=basic)
        if listUsers.status_code == 200:
            return listUsers.json()

    # overrideUser method:
    #
    # this method receives a User with new parameters that needs an update in the database
    # it patches the User via the Airflow Rest API unless the User does not exist
    # if the User's status is inactive his privileges get updated to "none",
    # otherwise if it's active his privileges get updated to the new ones
    #
    # overrideUsername: str
    # overrideStatus: str
    # overridePrivilege: str
    # overridePassword: str
    # overrideAddress: str
    # getOverrideUser: API call Response
    # overridePayload: Payload of strings + "roles" is an Array of [{str : str}]
    # patchOverrideUser: API call Response

    def overrideUser(self, overrideUser: User, basic: (str, str)):
        overrideUsername = overrideUser.getUsername()
        overrideStatus = overrideUser.getStatus()
        overridePrivilege = overrideUser.getPrivilege()
        overridePassword = overrideUser.getPassword()

        # now we build our api call address
        overrideAddress = keys.airflow_address + "api/v1/users/" + overrideUsername
        getOverrideUser = requests.get(overrideAddress, auth=basic)

        # we check if the response is what we wanted

        if getOverrideUser.status_code != 200:
            raise UserExistsException("")
        # if the override status is inactive we don't want to update their privilege

        elif overrideStatus == "inactive":
            overridePrivilege = "Public"

        # this are the parameters that will get changed

        overridePayload = {
            "email": overrideUsername,
            "first_name": ".",
            "last_name": ".",
            "roles": [{"name": overridePrivilege}],
            "username": overrideUsername,
        }
        # we patch the user

        patchOverrideUser = requests.patch(
            overrideAddress, json=overridePayload, auth=basic
        )

        # and check the response

        if patchOverrideUser.status_code != 200:
            raise UserExistsException("")

    # deleteUser method:
    #
    # this method receives a User that needs to be deleted
    # and deletes the User via the Airflow Rest API unless the Username doesn't exist
    # in the database
    #
    # deleteUsername: str
    # deleteUserAddress: str
    # deleteUserCode: API call Response

    def deleteUser(self, deleteUser: User, basic: (str, str)):
        deleteUsername = deleteUser.getUsername()

        # we build our address

        deleteUserAddress = keys.airflow_address + "api/v1/users/" + deleteUsername

        # delete the User via the api call

        deleteUserCode = requests.delete(deleteUserAddress, auth=basic)

        # and check the Response (204 is success)

        if deleteUserCode.status_code != 204:
            raise UserExistsException("")

    # createUser:
    #
    # this method receives Username, Password and a repetition of Password
    # Firstly if Password and the repeated Password don't match, an Exception is thrown.
    # Else if the Username is already taken a UserExistsException will get thrown.
    # If not, a new User with the given Username and Password gets created via the Airflow Rest API
    #
    # createUserPayload: Payload of strings + "roles" is an Array of [{str : str}]
    # createUserStatusCode: API call Response

    def createUser(
        self,
        signUpUsername: str,
        signUpPassword: str,
        signUpPasswordRepetition: str,
        basic: (str, str),
    ):
        # we check if the passwords are identical

        if signUpPassword != signUpPasswordRepetition:
            raise SignUpException("")

        # we build our address

        createUserAddress = keys.airflow_address + "api/v1/users"

        # this is the Payload we use to create the User
        createUserPayload = {
            "email": signUpUsername,
            "first_name": ".",
            "last_name": ".",
            "roles": [{"name": "Public"}],
            "username": signUpUsername,
            "password": signUpPassword,
        }

        # we make the API call to create the User
        createUserStatusCode = requests.post(
            createUserAddress, json=createUserPayload, auth=basic
        )

        # and check the response
        if createUserStatusCode.status_code != 200:
            raise UserExistsException("")

    # auxiliary method for testing
    def deleteAllUsers(self, basic: (str, str)):
        details = self.getAllUsersAndDetails(basic)
        for user in dict(details)[keys.all_users]:
            username: str = dict(user)["username"]
            if username != "airflow":
                delete_address = keys.airflow_address + "api/v1/users/" + username
                # delete the User via the api call
                response = requests.delete(delete_address, auth=basic)

                # and check the Response (204 is success)
                if response.status_code != 204:
                    raise InternalException("Internal Error in delete_all_users")
