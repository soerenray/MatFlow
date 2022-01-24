from array import array
from User import User
from requests.auth import HTTPBasicAuth
import requests



class UserController:
    # the authentification that's needed to do the Airflow Rest API calls
    _basic = HTTPBasicAuth()

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

    def getAllUsersAndDetails(self):
        listUsers = requests.get("http://localhost:8080/api/v1/users", auth = self.getAuth)
        if listUsers.status_code == 200:
            return listUsers.json()

    
    # overrideUser method:
    #
    # this method receives a User with new parameters that needs an update in the database
    # it patches the User via the Airflow Rest API unless the User does not exist
    # if the User's status is inactive his privileges get updated to "none",
    # otherwise if it's active his privileges get updated to the new ones

    def overrideUser(self, overrideUser: User):
        overrideUsername = overrideUser.getUsername
        overrideStatus = overrideUser.getStatus
        overridePrivilege = overrideUser.getPrivilege
        overridePassword = overrideUser.getPassword
        overrideAddress = "http://localhost:8080/api/v1/users/" + overrideUsername
        getOverrideUser = requests.get(overrideAddress, auth = self.getAuth)
        if getOverrideUser.status_code != 200:
            return "UserExistsException"
        elif overrideStatus == "inactive":
            overridePrivilege = None
        overridePayload = {
               "email": "", "first_name": "", "last_name": "", "roles": [{"name": overridePrivilege}], "username": overrideUsername, "password": overridePassword}
        patchOverrideUser = requests.patch(overrideAddress, json = overridePayload, auth = self.getAuth)
        if patchOverrideUser.status_code != 200:
            return "UserExistsException"


    # deleteUser method:
    #
    # this method receives a User that needs to be deleted
    # and deletes the User via the Airflow Rest API unless the Username doesn't exist 
    # in the database

    def deleteUser(self, deleteUser: User):
        deleteUsername = deleteUser.getUsername
        deleteUserAddress = "http://localhost:8080/api/v1/users/" + deleteUsername
        deleteUserCode = requests.delete(deleteUserAddress, auth = self.getAuth)
        if deleteUserCode.status_code != 200:
            return "UserExistsException"


    # loginUser method:
    #
    # this method receives Username and Password and confirms if the login
    # has been successfull.
    # If not the method throws the loginException

    def loginUser(self, loginUsername: str, loginPassword: str):
        loginUserAddress = "http://localhost:8080/api/v1/users/" + loginUsername
        if requests.get(loginUserAddress, auth = self.getAuth).json()["password"] != loginPassword:
            return "loginException"


    # createUser:
    #
    # this method receives Username, Password and a repetition of Password
    # Firstly if Password and the repeated Password don't match, an Exception is thrown.
    # Else if the Username is already taken a UserExistsException will get thrown.
    # If not, a new User with the given Username and Password gets created via the Airflow Rest API
    
    def createUser(self, signUpUsername: str, signUpPassword: str, signUpPasswordRepetition: str):
        if signUpPassword != signUpPasswordRepetition:
            return "signUpException"
        createUserAddress = "http://localhost:8080/api/v1/users"
        createUserPayload = {
               "email": "", "first_name": "", "last_name": "", "roles": [{"name": None}], "username": signUpUsername, "password": signUpPassword}
        createUserStatusCode = requests.post(createUserAddress, json =createUserPayload, auth = self.getAuth)
        if createUserStatusCode.status_code != 200:
            return "UserExistsException"
        

