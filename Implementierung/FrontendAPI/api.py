from __future__ import annotations
from pathlib import Path
from typing import List
from flask import Flask, request
from waitress import serve
from Implementierung.ExceptionPackage.MatFlowException import MatFlowException
from Implementierung.FrontendAPI import utilities
from Implementierung.UserAdministration.UserController import UserController
from Implementierung.UserAdministration.User import User
from Implementierung.workflow.frontend_version import FrontendVersion
from Implementierung.workflow.reduced_config_file import ReducedConfigFile
from Implementierung.workflow.template import Template
from Implementierung.workflow.version import Version
from Implementierung.workflow.workflow_manager import WorkflowManager
from .ExceptionHandler import ExceptionHandler
from Implementierung.HardwareAdministration.Hardware_Controller import Hardware_Controller
from Implementierung.HardwareAdministration.Server import Server
import keys

# according to Flask docs this command should be on modular level
app = Flask('FrontendAPI')
# max file upload size is 100 MB
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
    # we only have one server in system, and it needs to be pre-registered
    server: Server = Server()
    workflow_manager: WorkflowManager = WorkflowManager.get_instance()
    user_controller: UserController = UserController()
    hardware_controller: Hardware_Controller = Hardware_Controller(server)

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
            # api already up and running
            pass

    @classmethod
    def __start_api(cls):
        # serve(app, host="127.0.0.1", port=5000)
        app.run(debug=True)

    @staticmethod
    @app.route('/', methods=['GET', 'POST'])
    def default_get():
        return ExceptionHandler.success(dict())

    @staticmethod
    @app.route('/get_server_details', methods=['GET'])
    def get_server_details() -> str:
        """
        gets all server details (servername, ip address, cpu resources, gpu resources, selected for execution,
        container limit, status) and returns them in a json format

        Returns:
            String: json-dumped object containing the above described information
        """
        encoded_server: dict = Server.encode_server(FrontendAPI.hardware_controller.getServer())
        return ExceptionHandler.success(encoded_server)

    @staticmethod
    @app.route('/set_server_details', methods=['PUT'])
    def set_server_details() -> str:
        """
        sets all server details (servername, ip address, cpu resources, gpu resources, selected for execution, container
        limit, status)

        Returns:
            String: response indicating successful request
        """
        try:
            server: Server = Server.extract_server(request.get_json())
            FrontendAPI.hardware_controller.writeServer(server)
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route('/get_all_users_and_details', methods=['GET'])
    def get_all_users_and_details() -> str:
        """
        gets all users and their details (usernames, privileges, statuses) in a json format

        Returns:
             String: json-dumped object containing the above described information
        """
        # TODO Rückgabe mit Nils abchecken
        return ExceptionHandler.success(FrontendAPI.user_controller.getAllUsersAndDetails())

    @staticmethod
    @app.route('/set_user_details', methods=['PUT'])
    def set_user_details() -> str:
        """
        sets all user details (username, privilege, status) for a specific user in a json format.

        Returns:
            String: response indicating successful request
        """

        user: User = User.extract_user(request)
        user.setStatus(request.args.get(keys.user_status_name))
        user.setPrivilege(request.args.get(keys.user_privilege_name))
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

        Returns:
            String: response indicating successful request
        """
        user: User = User.extract_user(request)
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

        Returns:
            String: json-dumped object which contains all encoded versions
        """
        out_dict = dict()
        versions: List[FrontendVersion] = FrontendAPI.workflow_manager.get_versions_from_workflow_instance(
            request.args.get(keys.workflow_instance_name))
        for version in versions:
            out_dict.update(version.encode_version())
        return ExceptionHandler.success(out_dict)

    @staticmethod
    @app.route('/replace_wf_instance_active_version', methods=['PUT'])
    def replace_wf_instance_active_version() -> str:
        """
        replaces the specified workflow instance’s active version

        Returns:
            String: response indicating successful request
        """
        try:
            FrontendAPI.workflow_manager.set_active_version_through_number(
                request.args.get(keys.workflow_instance_name), request.args.get(keys.version_number_name))
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route('/create_version_of_wf_instance', methods=['POST'])
    def create_version_of_wf_instance() -> str:
        """
        changes multiple config files based on input/ key value pair changes in
        client’s applications during workflow instance configuration (request contains the changed config files name,
         all key value pairs per config file, contains workflow instance name)

        Returns:
            String: response indicating successful request
        """
        wf_instance_name: str = request.args.get(keys.workflow_instance_name)
        version_note: str = request.args.get(keys.version_note_name)
        # TODO Hier jeweils Listen
        configs_path: Path = Path(JSONToPython.extract_configs(request))
        try:
            FrontendAPI.workflow_manager.create_new_version_of_workflow_instance(wf_instance_name,
                                                                                 configs_path, version_note)
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route('/get_config_from_wf_instance', methods=['GET'])
    def get_config_from_wf_instance() -> str:
        """
        gets config file by workflow instance name and associated config file name (contains the wanted workflow
        instance name and its respective version and config file name)

        Returns:
            String: json-dumped object containing encoded config file
        """
        file: ReducedConfigFile = \
            FrontendAPI.workflow_manager.get_key_value_pairs_from_config_file(
                request.args.get(keys.workflow_instance_name), request.args.get(keys.config_file_name))
        return ExceptionHandler.success(file.encode_config())

    @staticmethod
    @app.route('/create_workflow_instance', methods=['POST'])
    def create_workflow_instance() -> str:
        """
        creates a new workflow instance via encoded workflow instance

        Returns:
            String: response indicating successful request
        """
        wf_instance_name: str = request.args.get(keys.workflow_instance_name)
        template_name: str = request.args.get(keys.template_name)
        # TODO hier auch Schleife
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
        # TODO andere Konvention
        wf_instances: List[str] = FrontendAPI.workflow_manager.get_names_of_workflows_and_config_files()[0]
        configs: List[str] = FrontendAPI.workflow_manager.get_names_of_workflows_and_config_files()[1]
        out_dict = {keys.workflow_instance_names: wf_instances, keys.config_file_names: configs}
        return ExceptionHandler.success(out_dict)

    @staticmethod
    @app.route('/verify_login', methods=['GET'])
    def verify_login() -> str:
        """
        verifies username with associated password via username and password

        Returns:
            String: response indicating successful request
        """
        try:
            FrontendAPI.user_controller.loginUser(request.args.get(keys.user_name),
                                                  request.args.get(keys.password_name))
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route('/register_user', methods=['POST'])
    def register_user() -> str:
        """
        registers a new user via new username and password (and repeated password)

        Returns:
            String: response indicating successful request
        """
        try:
            FrontendAPI.user_controller.createUser(request.args.get(keys.user_name),
                                                   request.args.get(keys.password_name),
                                                   request.args.get(keys.repeat_password_name))
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route('/create_template', methods=['POST'])
    def create_template() -> str:
        """
        creates a new template via encoded template

        Returns:
            String: response indicating successful request
        """
        try:
            template: Template = Template.extract_template(request)
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
        return ExceptionHandler.success({keys.template_names: FrontendAPI.workflow_manager.get_template_names()})

    @staticmethod
    @app.route('/get_template', methods=['GET'])
    def get_template() -> str:
        """
        gets wanted template by name

        Returns:
            String: json-dumped object containing encoded template
        """
        name = request.args.get(keys.template_name)
        try:
            template: Template = FrontendAPI.workflow_manager.get_template_from_name(name)
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        else:
            return ExceptionHandler.success(Template.encode_template(template))

    @staticmethod
    @app.route('/get_graph_for_temporary_template', methods=['GET'])
    def get_graph_for_temporary_template() -> str:
        """
        gets a preview picture of the DAG (used when in editor preview mode) via encoded template

        Returns:
            File: picture of dag in .png format
        """
        try:
            contemporary_template: Template = Template.extract_template(request)
            FrontendAPI.workflow_manager.create_template(contemporary_template)
            file_path: Path = FrontendAPI.workflow_manager.get_dag_representation_from_template(contemporary_template)
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        else:
            return ExceptionHandler.success(utilities.encode_file(file_path, keys.dag_picture_name))


###################################
# The Flask webserver entry point #
###################################

if __name__ == "__main__":
    a = FrontendAPI.get_frontend_api()