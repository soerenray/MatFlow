from typing import List, Tuple
from Implementierung.HardwareAdministration import Server
from Implementierung.UserAdministration import User, UserController
from Implementierung.workflow.template import Template
from Implementierung.workflow.reduced_config_file import ReducedConfigFile
from flask import request


class JSONToPython:

    """
    This class converts all json data into the wanted object by extracting certain keys and values and
    instantiating a new (temporary) object which executes the wanted methods (e.g. extract server and
    then execute set new container limit). Instantiated objects will be deleted by the garbage collection
    after they are finished writing back / getting data from the database.
    """
    @staticmethod
    def extract_user(request_details: request) -> User:
        """
        extracts json details and builds a new User based off of these json details

        Args:
            request_details(request): contains encoded user

        Returns:
            User: decoded user object
        """
        user_name: str = request_details.args.get('userName')
        controller: UserController = UserController()
        user: User = controller.getUser(user_name)
        return user


    @staticmethod
    def extract_server(request_details: request) -> Server:
        """
        extracts json details and builds a new Server based off of these json details

        Args:
            request_details(request): contains encoded server

        Returns:
            Server: decoded server object
        """
        name: str = request_details.args.get('serverName')
        ip_address: str = request_details.args.get('serverAddress')
        status: str = request_details.args.get('serverStatus')
        container_limit: int = request_details.args.get('containerLimit')
        resources: List[Tuple[str, str]] = request_details.args.get('serverResources')
        executing: bool = request_details.args.get('selectedForExecution')
        server: Server = Server(name, ip_address, status, container_limit, executing, resources)
        return server

    @staticmethod
    def extract_template(json_details: str) -> Template:
        """
        extracts json details and builds a new Template based off of these json details

        Args:
            json_details(String): contains encoded template

        Returns:
            Template: decoded template object
        """
        pass

    @staticmethod
    def extract_configs(request_details: request) -> List[ReducedConfigFile]:
        """
        extracts json details and builds a new ReducedConfigFile array based off of these json details

        Args:
            request_details(request): contains encoded reduced config files

        Returns:
            ReducedConfigFile[]: array of reduced config files
        """
        files: List[dict] = request.args.get('configFolder')
        for config in files:
            #config file name rausziehen
            # key value Paare sind in Liste -> rausziehen
            continue
