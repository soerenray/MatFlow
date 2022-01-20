from __future__ import annotations

from pathlib import Path
from typing import List

from flask import Flask, request
from waitress import serve
from Implementierung.ExceptionPackage.MatFlowException import MatFlowException
from Implementierung.workflow.frontend_version import FrontendVersion
from Implementierung.workflow.reduced_config_file import ReducedConfigFile
from Implementierung.workflow.template import Template
from Implementierung.workflow.workflow_manager import WorkflowManager
from JSONToPython import JSONToPython
from PythonToJSON import PythonToJSON
from ExceptionHandler import ExceptionHandler
from Implementierung.HardwareAdministration import Server, Hardware_Controller
from Implementierung.UserAdministration import User, UserController

# according to Flask docs this command should be on modular level
app = Flask('FrontendAPI')
# max file upload size is 100MB
app.config['MAX_CONTENT_LENGTH'] = 100000000
# allowed file extensions
app.config['UPLOAD_EXTENSIONS'] = ['.png', '.geo', '.cfg', '.py', '.config', '.conf', '.sh', '.dat']


class FrontendAPI:
    """
    This class is the main interface of the whole application. The client application can
    communicate with this api through json calls.
    """

    # not in instance scope due to static methods (are **required** for flask)
    # Due to the fact that api method calls with parameters are not possible
    # all parameters are fetched via the flask request object (as suggested by docs)
    __instance = None
    workflow_manager: WorkflowManager = WorkflowManager.get_instance()
    user_controller: UserController = UserController()
    hardware_controller: Hardware_Controller = Hardware_Controller()

    def __init__(self):
        # all "instantiations" should be called over get_frontend_api
        raise RuntimeError("Call get_frontend_api()")

    @classmethod
    def get_frontend_api(cls):
        """
        returns the FrontendAPI in singleton design fashion, meaning there is only one instance of FrontendAPI
        in circulation at all times.

        Returns:
            FrontendAPI: singleton FrontendAPI object
        """
        if cls.__instance is None:
            cls.__start_api()
        else:
            pass

    @classmethod
    def __start_api(cls):
        # serve(app, host="127.0.0.1", port=5000)
        app.run(debug='true')

    @staticmethod
    @app.route('/', methods=['GET', 'POST'])
    def default_get():
        return ExceptionHandler.success(dict())

    @staticmethod
    @app.route('/get_server_details', methods=['GET'])
    def get_server_details() -> str:
        """
        gets all server details (servername, ip address, cpu resources, gpu resources, selected for execution, container limit, status) and
        returns them in a json format

        Args:
            json_details(String): contains the wanted server's ip address

        Returns:
            String: json-dumped object containing the above described information
        """
        encoded_server: str = PythonToJSON.encode_server(FrontendAPI.hardware_controller.getServer())
        return encoded_server

    @staticmethod
    @app.route('/set_server_details', methods=['POST'])
    def set_server_details() -> str:
        """
        sets all server details (servername, ip address, cpu resources, gpu resources, selected for execution, container limit, status)

        Args:
            json_details(String): contains the new values in json format

        Returns:
            String: response indicating successful request
        """
        try:
            server: Server = JSONToPython.extract_server(request.get_json())
            FrontendAPI.hardware_controller.writeServer(server)
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route('/get_all_users_and_details', methods=['GET'])
    def get_all_users_and_details() -> str:
        """
        gets all users and their details (user names, privileges, statuses) in a json format

        Returns:
             String: json-dumped object containing the above described information
        """
        return PythonToJSON.encode_users(FrontendAPI.user_controller.getAllUsersAndDetails())

    @staticmethod
    @app.route('/set_user_details', methods=['POST'])
    def set_user_details() -> str:
        """
        sets all user details (user name, privilege, status) for a specific user in a json format.

        Args:
            json_details(String): contains the user details

        Returns:
            String: response indicating successful request
        """

        user: User = JSONToPython.extract_user(request)
        status: str = request.args.get('userStatus')
        privilege: str = request.args.get('userPrivilege')
        user.setStatus(request.args.get('userStatus'))
        user.setPrivilege(request.args.get('userPrivilege'))
        try:
            FrontendAPI.user_controller.overrideUser(user)
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route('/delete_user', methods=['DELETE'])
    def delete_user() -> str:
        """
        deletes a user by username

        Args:
            json_details(String): contains username

        Returns:
            String: response indicating successful request
        """
        user: User = JSONToPython.extract_user(request)
        try:
            FrontendAPI.user_controller.deleteUser(user)
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route('/get_wf_instance_versions', methods=['GET'])
    def get_wf_instance_versions() -> str:
        """
        gets the versions associated with wanted workflow instance

        Args:
            json_details(String): contains workflow instance name

        Returns:
            String: json-dumped object which contains all encoded versions
        """
        versions: List[FrontendVersion] = FrontendAPI.workflow_manager.getVersionsFromWorkflowInstance(
            request.args.get('workflowInstanceName'))
        return PythonToJSON.encode_versions(versions)

    @staticmethod
    @app.route('/replace_wf_instance_active_version', methods=['POST'])
    def replace_wf_instance_active_version() -> str:
        """
        replaces the specified workflow instance’s active version

        Args:
            json_details(String): workflow instance name and version number

        Returns:
            String: response indicating successful request
        """
        try:
            FrontendAPI.workflow_manager.set_active_version_through_number(request.args.get('workflowInstanceName'),
                                                                           request.args.get('versionNumber'))
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route('/create_version_of_wf_instance', methods=['POST'])
    def create_version_of_wf_instance() -> str:
        """
        changes multiple config files based on input/ key value pair changes in
        client’s applications during workflow instance configuration

        Args:
            json_details(String): contains the changed config files name, all key value pairs per config
            file, contains workflow instance name

        Returns:
            String: response indicating successful request
        """
        wf_instance_name: str = request.args.get('workflowInstanceName')
        version_note: str = request.args.get('versionNote')
        configs_path: Path = Path(JSONToPython.extract_configs(request))
        try:
            FrontendAPI.workflow_manager.create_new_version_of_workflow_instance(wf_instance_name, configs_path, version_note)
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route('/get_config_from_wf_instance', methods=['GET'])
    def get_config_from_wf_instance() -> str:
        """
        gets config file by workflow instance name and associated config file name

        Args:
            json_details(String): contains the wanted workflow instance name and its respective version and
            config file name

        Returns:
            String: json-dumped object containing encoded config file
        """
        file: ReducedConfigFile = \
            FrontendAPI.workflow_manager.get_key_value_pairs_from_config_file(request.args.get('workflowInstanceName'),
                                                                              request.args.get('configFileName'))
        return PythonToJSON.encode_config(file)

    @staticmethod
    @app.route('/create_workflow_instance', methods=['POST'])
    def create_workflow_instance() -> str:
        """
        creates a new workflow instance

        Args:
            json_details(string): contains encoded workflow instance

        Returns:
            String: response indicating successful request
        """
        wf_instance_name: str = request.args.get('workflowInstanceName')
        template_name: str = request.args.get('templateName')
        files: Path = Path(JSONToPython.extract_configs(request))
        try:
            FrontendAPI.workflow_manager.create_workflow_instance_from_template(template_name, wf_instance_name, files)

        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route('/get_all_wf_instances_names_and_config_file_names', methods=['GET'])
    def get_all_wf_instances_names_and_config_files_names() -> str:
        """
        gets all config file and all workflow instances names

        Returns:
            String: json-dumped object containing all workflow instance names and config file names
        """
        wf_instances: List[str] = FrontendAPI.workflow_manager.get_names_of_workflows_and_config_files()[0]
        configs: List[str] = FrontendAPI.workflow_manager.get_names_of_workflows_and_config_files()[1]
        out_dict = {'workflowInstanceNames': wf_instances, 'configFileNames': configs}
        return ExceptionHandler.success(out_dict)

    @staticmethod
    @app.route('/verify_login', methods=['GET'])
    def verify_login() -> str:
        """
        verifies username with associated password

        Args:
            json_details(String): contains username and password

        Returns:
            String: response indicating successful request
        """
        try:
            FrontendAPI.user_controller.login(request.args.get('userName'), request.args.get('password'))
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route('/register_user', methods=['POST'])
    def register_user() -> str:
        """
        registers a new user

        Args:
            json_details(String): contains new username and password (and repeated password)

        Returns:
            String: response indicating successful request
        """
        try:
            FrontendAPI.user_controller.createUser(userName=request.args.get('userName'),
                                                   password=request.args.get('password'),
                                                   repeatPassword=request.args.get('repeatPassword'))
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route('/create_template', methods=['POST'])
    def create_template(json_details: str) -> str:
        """
        creates a new template

        Args:
            json_details(String): contains encoded template

        Returns:
            String: response indicating successful request
        """
        name: str = request.args.get('templateName')
        file_path: Path = JSONToPython.extract_dag_file(request)
        try:
            template: Template = Template(name, file_path)
            FrontendAPI.workflow_manager.create_template(template)
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route('/get_all_template_names', methods=['GET'])
    def get_all_template_names() -> str:
        """
        gets all template names that are registered

        Returns:
            String: json-dumped object that contains all template names
        """
        return ExceptionHandler.success({'templateNames': FrontendAPI.workflow_manager.get_template_names()})

    @staticmethod
    @app.route('/get_template', methods=['GET'])
    def get_template(json_details: str) -> str:
        """
        gets wanted template

        Args:
            json_details(String): contains wanted template name

        Returns:
            String: json-dumped object conatining encoded template
        """
        name = request.args.get('templateName')
        try:
            template: Template = FrontendAPI.workflow_manager.get_template_from_name(name)
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        else:
            return PythonToJSON.encode_template(template)

    @staticmethod
    @app.route('/get_graph_for_temporary_template', methods=['GET'])
    def get_graph_for_temporary_template(json_details: str) -> str:
        """
        gets a preview picture of the DAG (used when in editor preview mode)

        Args:
            json_details(String): contains encoded template

        Returns:
            File: picture of dag in .png format
        """
        template: Template = FrontendAPI.workflow_manager.get_template_from_name(request.args.get('templateName'))
        file_path: Path = FrontendAPI.workflow_manager.get_dag_representation_from_template(template)
        return ExceptionHandler.success(PythonToJSON.encode_file(file_path, 'dagPicture'))


###################################
# The Flask webserver entry point #
###################################

if __name__ == "__main__":
    a = FrontendAPI.get_frontend_api()
