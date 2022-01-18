



class Server:
    name: str
    address: str
    status: str
    containerLimit:int
    selectedForExecution:bool
    ressources = [str,str]

    #Konstruktor
    def __init__(self, name: str, address: str, status: str, containerLimit: int, selectedForExecution: bool, ressources =[str,str]):
        self.name = name
        self.address = address
        self.status = status
        self.containerLimit= containerLimit
        self.selectedForExecution = selectedForExecution
        self.ressources = ressources

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





