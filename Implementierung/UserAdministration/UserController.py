from array import array
from User import User
from requests.auth import HTTPBasicAuth
import requests
from Implementierung.ExceptionPackage.MatFlowException import UserExistsException, LoginException, SignUpException



class UserController:
    # the authentification that's needed to do the Airflow Rest API calls
    _basic = HTTPBasicAuth("","")

    # CONSTRUCTOR
    #
    # has no parameters and sets the own basic authentification
    def __init__(self):
        self._basic = HTTPBasicAuth("airflow", "airflow")





    # METHODS


    # Getter- and Setter Methods:
     
    # Authentication getter method:
    #
    # Returns the basic authentification

    def getAuth(self):
        return self._basic



    # Other Methods:

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

    def getAllUsersAndDetails(self):
        listUsers = requests.get("http://localhost:8080/api/v1/users", auth = self.getAuth())
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

    def overrideUser(self, overrideUser: User):
        overrideUsername = overrideUser.getUsername()
        overrideStatus = overrideUser.getStatus()
        overridePrivilege = overrideUser.getPrivilege()
        overridePassword = overrideUser.getPassword()
        overrideAddress = "http://localhost:8080/api/v1/users/" + overrideUsername
        getOverrideUser = requests.get(overrideAddress, auth = self.getAuth())
        if getOverrideUser.status_code != 200:
            raise UserExistsException
        elif overrideStatus == "inactive":
            overridePrivilege = "Public"
        overridePayload = {
               "email": ".", "first_name": ".", "last_name": ".", "roles": [{"name": overridePrivilege}], "username": overrideUsername, "password": overridePassword}
        patchOverrideUser = requests.patch(overrideAddress, json = overridePayload, auth = self.getAuth())
        if patchOverrideUser.status_code != 200:
            raise UserExistsException


    # deleteUser method:
    #
    # this method receives a User that needs to be deleted
    # and deletes the User via the Airflow Rest API unless the Username doesn't exist 
    # in the database
    #
    # deleteUsername: str
    # deleteUserAddress: str
    # deleteUserCode: API call Response

    def deleteUser(self, deleteUser: User):
        deleteUsername = deleteUser.getUsername()
        deleteUserAddress = "http://localhost:8080/api/v1/users/" + deleteUsername
        deleteUserCode = requests.delete(deleteUserAddress, auth = self.getAuth())
        if deleteUserCode.status_code != 200:
            raise UserExistsException


    # loginUser method:
    #
    # this method receives Username and Password and confirms if the login
    # has been successfull.
    # If not the method throws the loginException
    #
    #loginUserAddress: str

    def loginUser(self, loginUsername: str, loginPassword: str):
        loginUserAddress = "http://localhost:8080/api/v1/users/" + loginUsername
        if requests.get(loginUserAddress, auth = self.getAuth()).json()["password"] != loginPassword:
            raise LoginException


    # createUser:
    #
    # this method receives Username, Password and a repetition of Password
    # Firstly if Password and the repeated Password don't match, an Exception is thrown.
    # Else if the Username is already taken a UserExistsException will get thrown.
    # If not, a new User with the given Username and Password gets created via the Airflow Rest API
    #
    # createUserPayload: Payload of strings + "roles" is an Array of [{str : str}]
    # createUserStatusCode: API call Response
    
    def createUser(self, signUpUsername: str, signUpPassword: str, signUpPasswordRepetition: str):
        if signUpPassword != signUpPasswordRepetition:
            raise SignUpException
        createUserAddress = "http://localhost:8080/api/v1/users"
        createUserPayload = {
               "email": ".", "first_name": ".", "last_name": ".", "roles": [{"name": "Public"}], "username": signUpUsername, "password": signUpPassword}
        createUserStatusCode = requests.post(createUserAddress, json =createUserPayload, auth = self.getAuth())
        if createUserStatusCode.status_code != 200:
            raise UserExistsException
        

