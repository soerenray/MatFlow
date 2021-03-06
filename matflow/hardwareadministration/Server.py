from __future__ import annotations

import socket
import resource
import json
from typing import Tuple

from matflow.exceptionpackage.MatFlowException import ConverterException
from matflow.frontendapi import keys


class Server:
    name: str
    address: str
    status: str
    containerLimit: int
    selectedForExecution: bool
    cpuResource: resource
    vmemResource: resource

    # Konstruktor

    def __init__(self):
        self.name = "server"
        hostname = socket.gethostname()
        self.address = socket.gethostbyname(hostname)
        self.status: bool = self.checkStatus()
        self.containerLimit = 20
        self.selectedForExecution = True
        # self.cpuResource = resource.setrlimit(resource.RLIMIT_CORE, resource.RLIM_INFINITY)
        # self.vmemResource = resource.setrlimit(resource.RLIMIT_VMEM, resource.RLIM_INFINITY)
        self.cpuResource = resource.RLIMIT_CPU
        self.vmemResource = resource.RLIM_INFINITY

    # getter and setter methods
    # name getter method
    def getName(self):
        return self.name

    # name setter method
    def setName(self, name):
        self.name = name

    # address getter method
    def getAddress(self):
        return self.address

    # address setter method
    def setAddress(self, address):
        self.address = address

    # status getter method
    def getStatus(self):
        return self.status

    # status setter method
    def setStatus(self, status):
        self.status = status

    # containerlimit getter method
    def getContainerLimit(self):
        return self.containerLimit

    # containerlimit setter method
    def setContainerLimit(self, limit):
        self.containerLimit = limit

    # selected for execution getter method
    def isSelectedForExecution(self):
        return self.selectedForExecution

    # selected for execution setter method
    def setSelectedForExecution(self, selected):
        self.selectedForExecution = selected

    # Ressources getter method
    def getRessources(self) -> Tuple[str, str]:
        return str(self.vmemResource), str(self.cpuResource)

    # Ressources setter method
    def setRessources(self, ressources: Tuple[str, str]):
        self.cpuResource = ressources[1]
        self.vmemResource = ressources[0]

    # other methods:

    # check status method:
    def checkStatus(self):
        # scanner = nmap.PortScanner()
        # host = socket.gethostbyname(self.getAddress())
        # scanner.scan(host, "1","-v")
        # if scanner[host].state() == "UP":
        return True

    # else:
    #    return False

    @classmethod
    def extract_server(cls, json_details: str) -> Server:
        """
        extracts json details and builds a new Server based off of these json details

        Args:
            json_details(str): contains encoded server

        Returns:
            Server: decoded server object
        """
        decoded_json: dict = json.loads(json_details)
        keys_to_be_in = [
            keys.server_name,
            keys.server_address_name,
            keys.server_status_name,
            keys.container_limit_name,
            keys.server_resources_name,
            keys.selected_for_execution_name,
        ]
        for key in keys_to_be_in:
            if key not in decoded_json:
                raise ConverterException(key + "not in json")
        name: str = decoded_json[keys.server_name]
        ip_address: str = decoded_json[keys.server_address_name]
        status: str = decoded_json[keys.server_status_name]
        container_limit: int = int(decoded_json[keys.container_limit_name])
        resources: Tuple[str, str] = decoded_json[keys.server_resources_name]
        executing: bool = bool(decoded_json[keys.selected_for_execution_name])
        server: Server = Server()
        server.setName(name)
        server.setStatus(status)
        server.setRessources(resources)
        server.setSelectedForExecution(executing)
        server.setContainerLimit(container_limit)
        server.setAddress(ip_address)
        return server

    def encode_server(self) -> dict:
        """
        encodes all server attributes and dumps them into json object

        Returns:
            String: json-dumped object containing encoded server
        """
        name: str = self.getName()
        ip_address: str = self.getAddress()
        status: bool = self.getStatus()
        container_limit: int = self.getContainerLimit()
        executing: bool = self.isSelectedForExecution()
        resources: Tuple[str, str] = self.getRessources()
        out_dict: dict = {
            keys.server_name: name,
            keys.server_address_name: ip_address,
            keys.server_status_name: status,
            keys.container_limit_name: container_limit,
            keys.selected_for_execution_name: executing,
            keys.server_resources_name: resources,
        }
        return out_dict
