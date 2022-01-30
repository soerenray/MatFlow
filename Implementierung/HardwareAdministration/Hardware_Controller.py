from operator import truediv
from Implementierung.HardwareAdministration.Server import Server


class Hardware_Controller:
    Server: Server

# Constructor
    def __init__(self, Server: Server):
        self.Server = Server

    def __init__(self):
        self.Server = None

# Methods

    # method that gets a Server and adds it to the ServerList
    def addServer(Server):
        Server = Server
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




