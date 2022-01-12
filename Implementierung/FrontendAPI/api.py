from __future__ import annotations
from flask import Flask
from flask_restful import Resource, Api
from waitress import serve

app = Flask('FrontendAPI')

class FrontendAPI():

    """
    This class is the main interface of the whole application. The client application can
    communicate with this api through json calls.
    """

    #__app = None
    __instance = None


    def __init__(self):
        raise RuntimeError("Call get_frontend_api()")
        #self.get_frontend_api()

    @classmethod
    def get_frontend_api(self) -> FrontendAPI:
        """
        returns the FrontendAPI in singleton design fashion, meaning there is only one instance of FrontendAPI
        in circulation at all times.

        Returns:
            FrontendAPI: singleton FrontendAPI object
        """
        if self.__instance is None:
            # package name as Flask's import_name
            #self.__app = Flask('FrontendAPI')
            self.__start_api(self)
        else:
            pass

    def __start_api(self):
        #serve(app, host="127.0.0.1", port=5000)
        app.run(debug='true')

    @app.route('/')
    def default_get():
        return "Welcome", 200

    @app.route('/get_server_details')
    def get_server_details(json_details: str) -> str:
        """
        gets all server details (servername, ip address, cpu resources, gpu resources, selected for execution, container limit, status) and
        returns them in a json format

        Args:
            json_details(String): contains the wanted server's ip address

        Returns:
            String: json-dumped object containing the above described information
        """
        #hier wird der Server mit ip geholt
        a = {"Server_details: hi"}
        json_out = json.dumps(a)
        return json_out
        #return json

    def set_server_details(json_details: str) -> str:
        """
        sets all server details (servername, ip address, cpu resources, gpu resources, selected for execution, container limit, status)

        Args:
            json_details(String): contains the new values in json format

        Returns:
            String: response indicating successful request
        """
        pass

    def get_all_users_and_details() -> str:
        """
        gets all users and their details (user names, privileges, statuses) in a json format

        Returns:
             String: json-dumped object containing the above described information
        """
        pass
        # return json

    def set_user_details(json_details: str) -> str:
        """
        sets all user details (user name, privilege, status) for a specific user in a json format.
        If user does not already exist, one will be created.

        Args:
            json_details(String): contains the user details

        Returns:
            String: response indicating successful request
        """
        pass

    def delete_user(json_details: str) -> str:
        """
        deletes a user by username

        Args:
            json_details(String): contains username

        Returns:
            String: response indicating successful request
        """
        pass

    def get_wf_instance_versions(json_details: str) -> str:
        """
        gets the versions associated with wanted workflow instance

        Args:
            json_details(String): contains workflow instance name

        Returns:
            String: json-dumped object which contains all encoded versions
        """
        # return json
        pass

    def replace_wf_instance_active_version(json_details: str) -> str:
        """
        replaces the specified workflow instance’s active version

        Args:
            json_details(String): workflow instance name and version number

        Returns:
            String: response indicating successful request
        """
        pass

    def create_version_of_wf_instance(json_details: str) -> str:
        """
        changes multiple config files ba- sed on input/ key value pair changes in
        client’s applications during workflow instance configuration

        Args:
            json_details(String): contains the changed config files name, all key value pairs per config
            file, contains workflow instance name

        Returns:
            String: response indicating successful request
        """
        pass

    def get_config_from_wf_instance(json_details: str) -> str:
        """
        gets config file by workflow instance name and associated config file name

        Args:
            json_details(String): contains the wanted workflow instance name and its respective version and
            config file name

        Returns:
            String: json-dumped object containing encoded config file
        """
        pass
        #return json

    def create_workflow_instance(json_details: str) -> str:
        """
        creates a new workflow instance

        Args:
            json_details(string): contains encoded workflow instance

        Returns:
            String: response indicating successful request
        """
        pass

    def get_all_wf_instances_names_and_config_files_names() -> str:
        """
        gets all config file and all workflow instances names

        Returns:
            String: json-dumped object containing all workflow instance names and config file names
        """
        pass
        # return json

    def verify_login(json_details: str) -> str:
        """
        verifies username with associated password

        Args:
            json_details(String): contains username and password

        Returns:
            String: response indicating successful request
        """
        pass
        # return json

    def register_user(json_details: str) -> str:
        """
        registers a new user

        Args:
            json_details(String): contains new username and password (and repeated password)

        Returns:
            String: response indicating successful request
        """
        pass

    def create_template(json_details: str) -> str:
        """
        creates a new template

        Args:
            json_details(String): contains encoded template

        Returns:
            String: response indicating successful request
        """
        pass

    def get_all_template_names() -> str:
        """
        gets all template names that are registered

        Returns:
            String: json-dumped object that contains all template names
        """
        pass
        # return json

    def get_template(json_details: str) -> str:
        """
        gets wanted template

        Args:
            json_details(String): contains wanted template name

        Returns:
            String: json-dumped object conatining encoded template
        """
        pass
        # return json

    def get_graph_for_temporary_template(json_details: str) -> str:
        """
        gets a preview picture of the DAG (used when in editor preview mode)

        Args:
            json_details(String): contains encoded template

        Returns:
            File: picture of dag in .png format
        """
        pass
        #return file


#########################
## The Flask webserver ##
#########################



a = FrontendAPI.get_frontend_api()
