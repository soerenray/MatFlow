from User import User



class UserController:


    user: User

    #Konstruktor
    def __init__(self, user: User):
         self.user = user

    #getter and setter methods

    #getUser method
    def getUser(self):
        return self.user

    #setUser method
    def setUser(self,user):
        self.user = user

    #other methods

    def deleteUser(self, user: User):
    #stuff happening
    #
    #
    #
    

    def resetPassword(self, user: User, oldPassword: str, newPassword: str):
    #stuff happening
    #
    #
    #

    def setPrivilege(self, user: User, newPrivilege: str):
    #stuff happening
    #
    #
    #

    def activateUser(self, user: User):
    #stuff happening
    #
    #
    #
    