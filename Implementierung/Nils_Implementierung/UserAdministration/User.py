

class User:
    username: str
    status: str
    privilege: str

#Konstruktor
    def __init__(self,username: str, status: str, privilege: str):
        self.username = username
        self.status = status
        self.privilege = privilege

# getter and setter methods
    #username getter method
    def getUsername(self):
        return self.username

    #username setter method
    def setUsername(self, username):
        self.username = username


    #status getter method
    def getStatus(self):
        return self.status

    #status setter method
    def setStatus(self, status):
        self.status = status

    #privilege getter method
    def getPrivilege(self):
        return self.privilege
    
    #privilege setter method
    def setPrivilege(self, priv):
        self.privilege = priv

