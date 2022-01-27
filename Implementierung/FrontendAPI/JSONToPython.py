from pathlib import Path
from typing import List, Tuple
import os
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from Implementierung.HardwareAdministration import Server
from Implementierung.UserAdministration import User, UserController
from Implementierung.workflow.template import Template
from Implementierung.workflow.reduced_config_file import ReducedConfigFile
from flask import request
import keys


class JSONToPython:

    """
    This class converts all json data into the wanted object by extracting certain keys and values and
    instantiating a new (temporary) object which executes the wanted methods (e.g. extract server and
    then execute set new container limit). Instantiated objects will be deleted by the garbage collection
    after they are finished writing back / getting data from the database.
    """

    parent_path: Path = Path(os.getcwd()).parent
    temp_in_path: str = os.path.join(parent_path, keys.temp_in_name)

    @staticmethod
    def extract_user(request_details: request) -> User:
        """
        extracts json details and builds a new User based off of these json details

        Args:
            request_details(request): contains encoded user

        Returns:
            User: decoded user object
        """
        user_name: str = request_details.args.get(keys.user_name)
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
        name: str = request_details.args.get(keys.server_name)
        ip_address: str = request_details.args.get(keys.server_address_name)
        status: str = request_details.args.get(keys.user_status_name)
        container_limit: int = int(request_details.args.get(keys.container_limit_name))
        resources: List[Tuple[str, str]] = request_details.args.get(keys.server_resources_name)
        executing: bool = bool(request_details.args.get(keys.selected_for_execution_name))
        server: Server = Server(name, ip_address, status, container_limit, executing, resources)
        return server

    @staticmethod
    def extract_template(request_details: request) -> Template:
        """
        extracts json details and builds a new Template based off of these json details

        Args:
            request_details(String): contains encoded template

        Returns:
            Template: decoded template object
        """
        name: str = request_details.args.get(keys.template_name)
        file_path: Path = JSONToPython.extract_dag_file(request_details)
        template: Template = Template(name, file_path)
        return template

    @staticmethod
    def extract_configs(request_details: request) -> str:
        """
        extracts json details and builds a new ReducedConfigFile array based off of these json details

        Args:
            request_details(request): contains encoded reduced config files

        Returns:
            ReducedConfigFile[]: array of reduced config files
        """
        save_dir: str = JSONToPython.create_dir(os.path.join(JSONToPython.parent_path, JSONToPython.temp_in_path,
                                                             keys.config_save_path))
        uploaded_files: List[FileStorage] = request_details.files.getlist(keys.files_key)
        # TODO dump in dir
        for counter in range(len(uploaded_files)):
            name: str = request.args.get(keys.config_file_name)[counter]
            file_path: str = os.path.join(save_dir, name)
            uploaded_files[counter].save(file_path)
            reduced_config: ReducedConfigFile = ReducedConfigFile(name, file_path)

        return save_dir

    @staticmethod
    def extract_dag_file(request_details: request) -> Path:
        """
        extracts json details and saves the dag definition file to the hard drive

        Args:
            request_details(request): contains dag definition file

        """

        dag_file: FileStorage = request_details.files[keys.file_key]
        filename: str = secure_filename(dag_file.filename)
        save_dir: str = JSONToPython.create_dir(os.path.join(JSONToPython.parent_path, JSONToPython.temp_in_path,
                                                             keys.dag_save_path))
        file_path: str = os.path.join(save_dir, filename)
        dag_file.save(file_path)
        return Path(file_path)

    @staticmethod
    def create_dir(path: str) -> str:
        """
        creates a directory with unique identifier to prevent overwriting
        """
        created_dir: bool = False
        counter: int = 0
        while not created_dir:
            try_path: str = os.path.join(path, keys.underscore, str(counter))
            if os.path.isdir(try_path):
                os.makedirs(try_path)
                return try_path
            counter += 1
