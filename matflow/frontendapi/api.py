from __future__ import annotations

import json
import os.path
import traceback
from pathlib import Path
from typing import List

# import requests.utils
# from deprecated import deprecated
from flask import Flask, request

# for production api:
from matflow.exceptionpackage.MatFlowException import (
    MatFlowException,
    ConverterException,
    AirflowConnectionException,
    LoginException,
)
from requests.exceptions import ConnectionError
from matflow.frontendapi import utilities, keys
from matflow.useradministration.UserController import UserController
from matflow.useradministration.User import User
from matflow.workflow.frontend_version import FrontendVersion
from matflow.workflow.reduced_config_file import ReducedConfigFile
from matflow.workflow.template import Template
from matflow.workflow.workflow_manager import WorkflowManager
from .ExceptionHandler import ExceptionHandler
from matflow.hardwareadministration.Hardware_Controller import Hardware_Controller
from matflow.hardwareadministration.Server import Server

# according to Flask docs this command should be on modular level
app = Flask("frontendapi")
# max file upload size is 100 MB
app.config["MAX_CONTENT_LENGTH"] = 100000000
# allowed file extensions
app.config["UPLOAD_EXTENSIONS"] = [
    ".png",
    ".geo",
    ".cfg",
    ".py",
    ".config",
    ".conf",
    ".sh",
    ".dat",
]


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
    workflow_manager: WorkflowManager = WorkflowManager.get_instance()
    user_controller: UserController = UserController()
    hardware_controller: Hardware_Controller = Hardware_Controller()

    def __init__(self):
        # all "instantiations" should be called over get_frontend_api
        raise RuntimeError("Call get_frontend_api()")

    @classmethod
    def get_frontend_api(cls) -> Flask:
        """
        returns the frontendapi in singleton design fashion, meaning there is only one instance of frontendapi
        in circulation at all times.

        Returns:
            FrontendAPI: singleton frontendapi object
        """
        if cls.__instance is None:
            cls.__start_api()
            return app
        else:
            # api already up and running
            pass

    @classmethod
    def __start_api(cls):
        # serve(app, host="127.0.0.1", port=5000)
        app.run(debug=True, port=8082)

    @staticmethod
    @app.route("/", methods=["GET", "POST"])
    def default_get():
        return ExceptionHandler.success(dict())

    @staticmethod
    @app.route("/get_server_details", methods=["GET"])
    def get_server_details() -> str:
        """
        gets all server details (servername, ip address, cpu resources, gpu resources, selected for execution,
        container limit, status) and returns them in a json format

        Returns:
            String: json-dumped object containing the above described information
        """
        try:
            auth_tag = request.authorization
            server: Server = FrontendAPI.hardware_controller.getServer(auth_tag["username"], auth_tag["password"])
            encoded_server: dict = server.encode_server()
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        else:
            return ExceptionHandler.success(encoded_server)

    @staticmethod
    @app.route("/set_server_details", methods=["PUT"])
    def set_server_details() -> str:
        """
        sets all server details (servername, ip address, cpu resources, gpu resources, selected for execution, container
        limit, status)

        Returns:
            String: response indicating successful request
        """
        try:
            json_decoded = get_json_not_dict()
            server: Server = Server.extract_server(json_decoded)
            auth_tag = request.authorization
            FrontendAPI.hardware_controller.setServer(server, auth_tag["username"], auth_tag["password"])
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        except TypeError:
            return ExceptionHandler.handle_exception(
                ConverterException("false/ no json provided")
            )
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route("/get_all_users_and_details", methods=["GET"])
    def get_all_users_and_details() -> str:
        """
        gets all users and their details (usernames, privileges, statuses) in a json format

        Returns:
             String: json-dumped object containing the above described information
        """
        # This is how a response looks like
        # {'total_entries': 2, 'users': [
        # {'active': True, 'changed_on': '2022-02-24T21:16:07.771595', 'created_on': '2022-02-24T21:16:07.771470',
        # 'email': 'airflowadmin@example.com', 'fail_login_count': 0, 'first_name': 'Airflow',
        # 'last_login': '2022-02-25T14:40:36.356283', 'last_name': 'Admin', 'login_count': 183,
        # 'roles': [{'name': 'Admin'}], 'username': 'airflow'},
        # {'active': True, 'changed_on': '2022-02-25T08:49:46.339749', 'created_on': '2022-02-25T08:49:46.339308',
        # 'email': '.', 'fail_login_count': 0, 'first_name': '.', 'last_login': '2022-02-25T08:58:08.301726',
        # 'last_name': '.', 'login_count': 3, 'roles': [{'name': 'Admin'}], 'username': 'first_user'}]}
        try:
            auth_tag = request.authorization
            details = FrontendAPI.user_controller.getAllUsersAndDetails((auth_tag["username"], auth_tag["password"]))

        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        except ConnectionError:
            return ExceptionHandler.handle_exception(
                AirflowConnectionException("Start Airflow container")
            )
        else:
            list_of_users_airflow = details["users"]
            out_list = []
            for user in list_of_users_airflow:
                status = user["active"]
                name = user["username"]
                # "roles": [{"name": "Admin"}
                privilege = user["roles"][0]["name"]
                user_dict = {
                    keys.user_name: name,
                    keys.user_status_name: status,
                    keys.user_privilege_name: privilege,
                }
                out_list.append(user_dict)
            return ExceptionHandler.success({keys.all_users: out_list})

    @staticmethod
    @app.route("/set_user_details", methods=["PUT"])
    def set_user_details() -> str:
        """
        sets all user details (username, privilege, status) for a specific user in a json format.

        Returns:
            String: response indicating successful request
        """
        try:
            json_details = get_json_not_dict()
            auth_tag = request.authorization
            user: User = User.extract_user(json_details)
            FrontendAPI.user_controller.overrideUser(user, (auth_tag["username"], auth_tag["password"]))
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        except TypeError:
            return ExceptionHandler.handle_exception(
                ConverterException("false/ no json provided")
            )
        except ConnectionError:
            return ExceptionHandler.handle_exception(
                AirflowConnectionException("Start Airflow container")
            )
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route("/delete_user", methods=["DELETE"])
    def delete_user() -> str:
        """
        deletes a user by username

        Returns:
            String: response indicating successful request
        """
        try:
            json_details = get_json_not_dict()
            auth_tag = request.authorization
            user: User = User.extract_user(json_details)
            FrontendAPI.user_controller.deleteUser(user, (auth_tag["username"], auth_tag["password"]))
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        except TypeError:
            return ExceptionHandler.handle_exception(
                ConverterException("false/ no json provided")
            )
        except ConnectionError:
            return ExceptionHandler.handle_exception(
                AirflowConnectionException("Start Airflow container")
            )
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route("/get_wf_instance_versions", methods=["POST"])
    def get_wf_instance_versions() -> str:
        """
        gets the versions associated with wanted workflow instance

        Returns:
            String: json-dumped object which contains all encoded versions
        """
        out_dict: dict = dict()
        list_of_versions: List[dict] = []
        try:
            auth_tag = request.authorization
            loaded = json.loads(get_json_not_dict())
            check_routine([keys.workflow_instance_name], loaded)
            wf_name: str = loaded[keys.workflow_instance_name]
            versions: List[
                FrontendVersion
            ] = FrontendAPI.workflow_manager.get_versions_from_workflow_instance(
                wf_name
            )
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        except TypeError as e:
            return ExceptionHandler.handle_exception(
                ConverterException("false/ no json provided")
            )
        else:
            for version in versions:
                list_of_versions.append(version.encode_version())
            out_dict.update({keys.versions_name: list_of_versions})
            return ExceptionHandler.success(out_dict)

    @staticmethod
    @app.route("/replace_wf_instance_active_version", methods=["PUT"])
    def replace_wf_instance_active_version() -> str:
        """
        replaces the specified workflow instance’s active version

        Returns:
            String: response indicating successful request
        """
        try:
            auth_tag = request.authorization
            decoded_json: dict = json.loads(get_json_not_dict())
            check_routine([keys.workflow_instance_name, keys.version_number_name], decoded_json)
            FrontendAPI.workflow_manager.set_active_version_through_number(
                decoded_json[keys.workflow_instance_name],
                decoded_json[keys.version_number_name],
            )
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        except TypeError:
            return ExceptionHandler.handle_exception(
                ConverterException("false/ no json provided")
            )
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route("/create_version_of_wf_instance", methods=["POST"])
    def create_version_of_wf_instance() -> str:
        """
        changes multiple config files based on input/ key value pair changes in
        client’s applications during workflow instance configuration (request contains the changed config files name,
         all key value pairs per config file, contains workflow instance name)

        Returns:
            String: response indicating successful request
        """
        try:
            auth_tag = request.authorization
            decoded_json: dict = json.loads(get_json_not_dict())
            check_routine([keys.workflow_instance_name, keys.version_note_name], decoded_json)
            wf_instance_name: str = decoded_json[keys.workflow_instance_name]
            version_note: str = decoded_json[keys.version_note_name]
            configs: List[
                ReducedConfigFile
            ] = ReducedConfigFile.extract_multiple_configs(get_json_not_dict())
            FrontendAPI.workflow_manager.create_new_version_of_workflow_instance(
                wf_instance_name, configs, version_note
            )
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        except TypeError:
            return ExceptionHandler.handle_exception(
                ConverterException("false/ no json provided")
            )
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route("/get_config_from_wf_instance", methods=["POST"])
    def get_config_from_wf_instance() -> str:
        """
        gets config file by workflow instance name and associated config file name (contains the wanted workflow
        instance name and its respective version and config file name)

        Returns:
            String: json-dumped object containing encoded config file
        """
        try:
            auth_tag = request.authorization
            decoded_json: dict = json.loads(get_json_not_dict())
            check_routine([keys.workflow_instance_name, keys.config_file_name], decoded_json)
            wf_name: str = decoded_json[keys.workflow_instance_name]
            config_name: str = decoded_json[keys.config_file_name]
            file: ReducedConfigFile = (
                FrontendAPI.workflow_manager.get_key_value_pairs_from_config_file(
                    wf_name, config_name
                )
            )
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        except TypeError:
            return ExceptionHandler.handle_exception(
                ConverterException("false/ no json provided")
            )
        else:
            return ExceptionHandler.success(file.encode_config())

    @staticmethod
    @app.route("/create_workflow_instance", methods=["POST"])
    def create_workflow_instance() -> str:
        """
        creates a new workflow instance via encoded workflow instance

        Returns:
            String: response indicating successful request
        """
        try:
            auth_tag = request.authorization
            decoded_json: dict = json.loads(get_json_not_dict())
            check_routine([keys.workflow_instance_name, keys.template_name], decoded_json)
            wf_name: str = decoded_json[keys.workflow_instance_name]
            template_name: str = decoded_json[keys.template_name]
            files: Path = ReducedConfigFile.extract_multiple_config_files(
                get_json_not_dict()
            )
            FrontendAPI.workflow_manager.create_workflow_instance_from_template(
                template_name, wf_name, files
            )
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        except TypeError as e:
            return ExceptionHandler.handle_exception(
                ConverterException("false/ no json provided")
            )
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route("/get_all_wf_instances_names_and_config_file_names", methods=["GET"])
    def get_all_wf_instances_names_and_config_files_names() -> str:
        """
        gets all config file and all workflow instances names

        Returns:
            String: json-dumped object containing all workflow instance names and config file names
        """
        # the return is already in format {wf_instance_name_1: List[Config], wf_instance_name_2: List[Config], ..}
        # never an exception, worst case is empty dict
        return ExceptionHandler.success(
            {
                keys.names_and_configs: FrontendAPI.workflow_manager.get_names_of_workflows_and_config_files()
            }
        )

    @staticmethod
    @app.route("/verify_login", methods=["GET"])
    #  @deprecated(reason="Please use airflow login", version="1.0")
    def verify_login() -> str:
        """
        verifies username with associated password via username and password

        Returns:
            String: response indicating successful request
        """
        try:
            raise LoginException("Use airflow login")
            # decoded_json: dict = json.loads(get_json_not_dict())
            # check_routine([keys.user_name, keys.password_name], decoded_json)
            # FrontendAPI.user_controller.loginUser(
            #     decoded_json[keys.user_name], decoded_json[keys.password_name]
            # )
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        except TypeError:
            return ExceptionHandler.handle_exception(
                ConverterException("false/ no json provided")
            )
        except ConnectionError:
            return ExceptionHandler.handle_exception(
                AirflowConnectionException("Start Airflow container")
            )

    @staticmethod
    @app.route("/register_user", methods=["POST"])
    def register_user() -> str:
        """
        registers a new user via new username and password (and repeated password)

        Returns:
            String: response indicating successful request
        """
        try:
            auth_tag = request.authorization
            decoded_json: dict = json.loads(get_json_not_dict())
            keys_to_check = [keys.user_name, keys.password_name, keys.repeat_password_name]
            check_routine(keys_to_check, decoded_json)
            check_auth_tag(auth_tag)
            FrontendAPI.user_controller.createUser(
                decoded_json[keys.user_name],
                decoded_json[keys.password_name],
                decoded_json[keys.repeat_password_name],
                (auth_tag["username"], auth_tag["password"])
            )
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        except TypeError as error:
            return ExceptionHandler.handle_exception(
                ConverterException(
                    "false/ no json provided" + " Error: " + str(error.args)
                )
            )
        except ConnectionError:
            return ExceptionHandler.handle_exception(
                AirflowConnectionException("Start Airflow container")
            )
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route("/create_template", methods=["POST"])
    def create_template() -> str:
        """
        creates a new template via encoded template

        Returns:
            String: response indicating successful request
        """
        try:
            template: Template = Template.extract_template(get_json_not_dict())
            FrontendAPI.workflow_manager.create_template(template)
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        except TypeError as error:
            print(error.args)
            print(traceback.format_exc())
            return ExceptionHandler.handle_exception(
                ConverterException(
                    "false/ no json provided" + "Error: " + str(error.args)
                )
            )
        else:
            return ExceptionHandler.success(dict())

    @staticmethod
    @app.route("/get_all_template_names", methods=["GET"])
    def get_all_template_names() -> str:
        """
        gets all template names that are registered

        Returns:
            String: json-dumped object that contains all template names
        """
        return ExceptionHandler.success(
            {keys.template_names: FrontendAPI.workflow_manager.get_template_names()}
        )

    @staticmethod
    @app.route("/get_template", methods=["POST"])
    def get_template() -> str:
        """
        gets wanted template by name

        Returns:
            String: json-dumped object containing encoded template
        """
        try:
            decoded_json: dict = json.loads(get_json_not_dict())
            check_routine([keys.template_name], decoded_json)
            name = decoded_json[keys.template_name]
            template: Template = FrontendAPI.workflow_manager.get_template_from_name(
                name
            )
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        except TypeError:
            return ExceptionHandler.handle_exception(
                ConverterException("false/ no json provided")
            )
        else:
            return ExceptionHandler.success(template.encode_template(False))

    @staticmethod
    @app.route("/get_graph_for_temporary_template", methods=["GET"])
    def get_graph_for_temporary_template() -> str:
        """
        gets a preview picture of the DAG (used when in editor preview mode) via encoded template

        Returns:
            File: picture of dag in .png format
        """
        try:
            contemporary_template: Template = Template.extract_template(
                get_json_not_dict()
            )
            FrontendAPI.workflow_manager.create_template(contemporary_template)
            file_path: Path = (
                FrontendAPI.workflow_manager.get_dag_representation_from_template(
                    contemporary_template
                )
            )
        except MatFlowException as exception:
            return ExceptionHandler.handle_exception(exception)
        except TypeError:
            return ExceptionHandler.handle_exception(
                ConverterException("false/ no json provided")
            )
        else:
            out = utilities.encode_file(file_path, keys.dag_picture_name, True)
            # file is already removed in utilities.encode
            os.rmdir(file_path.parent)
            return ExceptionHandler.success(out)


def check_routine(keys_to_check: List[str], decoded_json: dict) -> None:
    for key in keys_to_check:
        if key not in decoded_json:
            raise TypeError("please provide: " + key)

def check_auth_tag(auth_tag: dict) -> None:
    # These are hard coded airflow requirements
    keys_to_check = ["username", "password"]
    check_routine(keys_to_check, auth_tag)


def get_json_not_dict() -> str:
    json_str: str
    if type(request.get_json()) != str:
        json_str = json.dumps(request.get_json())
    else:
        json_str = request.get_json()
    return json_str


###################################
# The Flask webserver entry point #
###################################

if __name__ == "__main__":
    a = FrontendAPI.get_frontend_api()
