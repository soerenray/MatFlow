from operator import truediv
import resource
from Implementierung.Database.ServerData import ServerData
from Implementierung.HardwareAdministration.Server import Server


class Hardware_Controller:
    _Server: Server

    # Constructor
    def __init__(self):
        standardServer = Server()
        self._Server = standardServer

    # Methods:

    # getServer method gets the standard server via his ip
    def getServer(self):
        tempServerData = ServerData()
        self._Server = tempServerData.get_server()
        return self._Server

    # writeServer
    def writeServer(self, newServer: Server):
        tempServerData = ServerData()
        tempServerData.write_server(newServer)

    # setCPUResources
    def setResources(self, newResource: resource, newSoft: int, newHard: int):
        resource.setrlimit(newResource, newSoft, newHard)

    # Methods

    # method that gets a Server and adds it to the ServerList
    def addServer(Server):
        Server = Server()
        # stuff that happens
        #
        #
        #
        #
        #
        #

    # method that gets a Server and a containerLimit
    # and sets the Server's containerLimit to the given number
    def changeContainerLimit(Server, containerLimit):
        Server.containerLimit = containerLimit
        # stuff that happens
        #
        #
        #
        #
        #

    # method that gets a Server and sets the Servers bool "isSelectedForExecution"
    # to True
    def selectServer(Server):
        Server.isSelectedForExecution = True
        # stuff that happens
        #
        #
        #
        #
        #
        #

    def getServer(self) -> Server:
        return self._Server

    def setServer(self, server: Server):
        self._Server = server
