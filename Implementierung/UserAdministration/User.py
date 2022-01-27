
# User class
#
# username: the Users Username
# status: the Users status (is either "active" or "inactive") 
# privilege: the Users privilege, no privilege equals inactive status 
# password: the Users password

class User:
    _username: str
    _status: str
    _privilege: str
    _password: str

# Construktor
    def __init__(self,username: str, status: str, privilege: str, password: str):
        self._username = username
        self._status = status
        self._privilege = privilege
        self._password = password

# getter and setter methods:

    #username getter method
    def getUsername(self):
        return self._username

    #username setter method
    def setUsername(self, username):
        self._username = username


    #status getter method
    def getStatus(self):
        return self._status

    #status setter method
    def setStatus(self, status):
        self._status = status

    #privilege getter method
    def getPrivilege(self):
        return self._privilege
    
    #privilege setter method
    def setPrivilege(self, priv):
        self._privilege = priv

    #password getter method
    def getPassword(self):
        return self._password
    
    #password setter method
    def setPrivilege(self, password):
        self._password = password 



