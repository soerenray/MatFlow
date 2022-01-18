from array import array
from User import User
import requests



class UserController:


    
    # Methods

    # getUser method
    # This method uses the username to get the wanted user via the airflow api

    # maybe like this?
    def getUser(self, username: str):
        user = requests.get("http://localhost:8080/api/v1/users/{username}", username)
        return user

    # getUsers method
    # This method returns all non deleted users
    def getUsers(self):
        users = requests.get("http://localhost:8080/api/v1/users")
        return users

    # createUser method
    # This method creates a new user using the given arguments via the airflow api

    
    def createUser(self, email: str, firstName: str, lastName: str, roles: array, username: str, password: str):
        statuscode = requests.post("http://localhost:8080/api/v1/users", {"email": email,"first_name": firstName,"last_name": lastName,"roles": roles,"username": username,"password": password})
        return statuscode


        

    # deleteUser method test1
    # This method uses the username to delete the wanted user via the airflow api
    # if the user does not exist the method returns a False boolean
    # if the user exists the method deletes the user and returns a True boolean
    #def deleteUser(self, username: str):
    #    user = requests.get("http://localhost:8080/api/v1/users/{username}")
    #    if user is None:
    #        return False
    #    else:
    #        requests.delete("http://localhost:8080/api/v1/users/{username}")
    #        return True

    # deleteUser method test2
    def deleteUser(self, username: str):    
        statuscode = requests.delete("http://localhost:8080/api/v1/users/{username}", username)
        return statuscode

    
    # resetPassword method
    # This method uses the username to get the wanted user and then updates the users password to the new password via the airflow api
    # The method returns the statuscode 200
    def resetPassword(self, username: str, newPassword: str):
        user = requests.get("http://localhost:8080/api/v1/users/{username}", username)
        statuscode = requests.patch("http://localhost:8080/api/v1/users/{username}",username,[user.email, user.first_name, user.last_name, user.roles, user.username, newPassword])
        return statuscode
    

    # setPrivilege method
    def setPrivilege(self, username: str, newPrivilege: str):
        user = requests.get("http://localhost:8080/api/v1/users/{username}", username)
        statuscode = requests.patch("http://localhost:8080/api/v1/users/{username}",username,[user.email, user.first_name, user.last_name, user.roles.append(newPrivilege), user.username, user.password])
        return statuscode
  

    # Bei der Methode weiß ich noch nicht wie ich sie mit der api implementieren kann
    # 
    # def activateUser(self, user: User):
    # stuff happening
    #
    #
    #
    