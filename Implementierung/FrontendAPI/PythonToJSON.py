import os
from pathlib import Path

from werkzeug.utils import secure_filename
from base64 import b64encode
from Implementierung.HardwareAdministration import Server
from Implementierung.UserAdministration import User
from typing import List
from ExceptionHandler import ExceptionHandler
from Implementierung.workflow import FrontendVersion
from Implementierung.workflow.template import Template
from Implementierung.workflow.reduced_config_file import ReducedConfigFile
from Implementierung.workflow.workflow_instance import WorkflowInstance
from Implementierung.workflow.version import Version


class PythonToJSON:
    """
    This class converts all python objects into json data by extracting certain keys and values and dumping them
    into a json object.
    """

    @staticmethod
    def encode_users(users: List[User]) -> str:
        """
        encodes all user attributes and dumps them into json object

        Args:
            users(List[User]): users whose attributes are to be encoded

        Returns:
            String: json-dumped object containing encoded user
        """

        out_dict = {}
        for user in users:
            out_dict.update({'userName': user.getUsername(), 'userStatus': user.getStatus(), 'userPrivilege':
                            user.getPrivilege()})
        return ExceptionHandler.success(out_dict)

    @staticmethod
    def encode_server(server: Server) -> str:
        """
        encodes all server attributes and dumps them into json object

        Args:
            server(Server): server whose attributes are to be encoded

        Returns:
            String: json-dumped object containing encoded server
        """
        name: str = server.getName()
        ip_address: str = server.getAddress()
        status: str = server.getStatus()
        container_limit: int = server.getContainerLimit()
        executing: bool = server.isSelectedForExecution()
        resources: list[tuple[str, str]] = server.getRessources()
        out_dict: dict = {'serverName': name, 'serverAddress': ip_address, 'serverStatus': status,
                          'containerLimit': container_limit, 'selectedForExecution': executing,
                          'serverResources': resources}
        return ExceptionHandler.success(out_dict)

    @staticmethod
    def encode_template(template: Template) -> str:
        """
        encodes all template attributes and dumps them into json object

        Args:
            template(Template): template whose attributes are to be encoded

        Returns:
            List[str]: all the needed information to upload file
        """
        out_dict: dict = dict()
        name: str = template.get_name()
        out_dict.update({'templateName': name})
        # path to file
        file_path: Path = template.get_dag_definition_file()
        out_dict.update(PythonToJSON.encode_file(file_path, 'dagDefinitionFile'))
        return ExceptionHandler.success(out_dict)

    @staticmethod
    def encode_wf_instance(wf_instance: WorkflowInstance) -> str:
        """
        encodes all workflow instance attributes and dumps them into json object

        Args:
            wf_instance(WorkflowInstance): workflow instance whose attributes are to be encoded

        Returns:
            String: json-dumped object containing encoded workflow instance
        """
        pass

    @staticmethod
    def encode_config(reduced_config: ReducedConfigFile) -> str:
        """
        extracts all reduced_config attributes and dumps them into json object

        Args:
            reduced_config(ReducedConfigFile): reduced config file whose attributes are to be encoded

        Returns:
            String: json-dumped object containing encoded reduced config file (essentially key value pairs)
        """
        out_dict = dict({'configFileName': reduced_config.get_file_name()})
        key_value_pairs_path: Path = reduced_config.get_key_value_pairs()
        out_dict.update(PythonToJSON.encode_file(key_value_pairs_path, 'keyValuePairs'))
        return ExceptionHandler.success(out_dict)

    @staticmethod
    def encode_versions(versions: List[FrontendVersion]) -> str:
        """
        extracts all version attributes of each version and dumps them into one json object
        Args:
            versions(str[]): array of version numbers

        Returns:
            String: json-dumped object containing encoded versions
        """
        all_versions = []
        for version in versions:
            version_dict = dict()
            version_dict.update({'versionNote': version.getNote()})
            version_dict.update({'versionNumber': version.getVersionNumber()})
            version_dict.update({'parameterChanges': version.getParameterChanges()})
            all_versions.append(version_dict)
        out_dict: dict = {'versions': all_versions}
        return ExceptionHandler.success(out_dict)

    @staticmethod
    def encode_file(file_path: Path, key: str) -> dict:
        out_dict: dict = dict()
        with open(file_path, "rb") as file:
            out_dict.update({key: b64encode(file.read())})
        os.remove(file_path)
        return out_dict
