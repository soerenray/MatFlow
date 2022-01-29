from __future__ import annotations

from typing import List, Tuple

from flask import request

from Implementierung.FrontendAPI import keys
from Implementierung.FrontendAPI.ExceptionHandler import ExceptionHandler


class Server:
    name: str
    address: str
    status: str
    containerLimit:int
    selectedForExecution:bool
    ressources = List[Tuple[str, str]]

    #Konstruktor
    def __init__(self, name: str, address: str, status: str, containerLimit: int, selectedForExecution: bool, ressources =List[Tuple[str, str]]):
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
    def getRessources(self) -> List[Tuple[str, str]]:
        return self.ressources

    # Ressources setter method
    def setRessources(self,ressources):
        self.ressources = ressources

    @classmethod
    def extract_server(cls, request_details: request) -> Server:
        """
        extracts json details and builds a new Server based off of these json details

        Args:
            request_details(request): contains encoded server

        Returns:
            Server: decoded server object
        """
        name: str = request_details.args.get(keys.server_name)
        ip_address: str = request_details.args.get(keys.server_address_name)
        status: str = request_details.args.get(keys.user_status_name)
        container_limit: int = int(request_details.args.get(keys.container_limit_name))
        resources: List[Tuple[str, str]] = request_details.args.get(keys.server_resources_name)
        executing: bool = bool(request_details.args.get(keys.selected_for_execution_name))
        server: Server = Server(name, ip_address, status, container_limit, executing, resources)
        return server

    def encode_server(self) -> dict:
        """
        encodes all server attributes and dumps them into json object

        Returns:
            String: json-dumped object containing encoded server
        """
        name: str = self.getName()
        ip_address: str = self.getAddress()
        status: str = self.getStatus()
        container_limit: int = self.getContainerLimit()
        executing: bool = self.isSelectedForExecution()
        resources: List[Tuple[str, str]] = self.getRessources()
        out_dict: dict = {keys.server_name: name, keys.server_address_name: ip_address, keys.server_status_name: status,
                          keys.container_limit_name: container_limit, keys.selected_for_execution_name: executing,
                          keys.server_resources_name: resources}
        return out_dict


