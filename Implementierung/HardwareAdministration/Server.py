
import nmap, socket
import resource


class Server:
    name: str
    address: str
    status: str
    containerLimit:int
    selectedForExecution:bool
    ressources = [str,str]

    #Konstruktor

    # TODO USE RESOURCE IMPORT FOR RESSOURCES
    def __init__(self):
        self.name = "server"
        self.address = "IP"
        self.status = self.checkStatus(self)
        self.containerLimit= 20
        self.selectedForExecution = True
        self.ressources = ["GPU", "unlimited"] + ["CPU", "unlimited"]

# getter and setter methods
    # name getter method
    def getName(self):
        return self.name

    # name setter method
    def setName(self,name):
        self.name = name

    # address getter method
    def getAddress(self):
        return self.address

    # address setter method
    def setAddress(self,address):
        self.address = address

    # status getter method
    def getStatus(self):
        return self.status

    # status setter method
    def setStatus(self,status):
        self.status = status

    # containerlimit getter method
    def getContainerLimit(self):
        return self.containerLimit

    # containerlimit setter method
    def setContainerLimit(self,limit):
        self.containerLimit = limit

    # selected for execution getter method
    def isSelectedForExecution(self):
        return self.selectedForExecution

    # selected for execution setter method
    def setSelectedForExecution(self, selected):
        self.selectedForExecution = selected

    # Ressources getter method
    def getRessources(self):
        return self.ressources

    # Ressources setter method
    def setRessources(self,ressources):
        self.ressources = ressources

    # other methods:

    # check status method:
    def checkStatus(self):
        scanner = nmap.PortScanner()
        host = socket.gethostbyname(self.getAddress)
        scanner.scan(host, "1","-v")
        if scanner[host].state() == "UP":
            return True
        else:
            return False
        




