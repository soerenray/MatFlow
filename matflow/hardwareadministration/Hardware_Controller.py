#import resource
from matflow.database import ServerData
from matflow.hardwareadministration.Server import Server
import requests
from requests.auth import HTTPBasicAuth


class Hardware_Controller:
    _Server: Server

    # Constructor
    def __init__(self):
        standardServer = Server()
        self._Server = standardServer

    # Methods:

    # getServer method gets the standard server via his ip
    def get_server(self):
        tempServerData = ServerData()
        self._Server = tempServerData.get_server()
        return self._Server

    # writeServer
    def writeServer(self, newServer: Server):
        tempServerData = ServerData()
        tempServerData.write_server(newServer)

    # setCPUResources
    #def setResources(self, newResource: resource, newSoft: int, newHard: int):
    #    resource.setrlimit(newResource, newSoft, newHard)

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

    def getServer(self, username: str, password: str) -> Server:
        hardware_auth = HTTPBasicAuth(username, password)
        search_user = username
        search_url = "http://localhost:8080/api/v1/users/" + search_user
        permission = requests.get(search_url, auth= hardware_auth).json()["roles"][0]["name"]
        if permission == "admin":
            tempServerData = ServerData()
            self._Server = tempServerData.get_server()
            return self._Server

    def setServer(self, server: Server, username:str, password: str):
        hardware_auth = HTTPBasicAuth(username, password)
        search_user = username
        search_url = "http://localhost:8080/api/v1/users/" + search_user
        permission = requests.get(search_url, auth=hardware_auth).json()["roles"][0]["name"]
        if permission == "admin":
            tempServerData = ServerData()
            tempServerData.write_server(server)
