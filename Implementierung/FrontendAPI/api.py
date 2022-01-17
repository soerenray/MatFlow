from __future__ import annotations
from flask import Flask, request
from waitress import serve
from Implementierung.Database.ServerData import ServerData
from Implementierung.ExceptionPackage.matflowexception import MatFlowException
from JSONToPython import JSONToPython
from ExceptionHandler import ExceptionHandler

# according to Flask docs this command should be on modular level

app = Flask('FrontendAPI')


class FrontendAPI:
    """
    This class is the main interface of the whole application. The client application can
    communicate with this api through json calls.
    """

    # __app = None
    __instance = None

    def __init__(self):
        raise RuntimeError("Call get_frontend_api()")
        # self.get_frontend_api()

    @classmethod
    def get_frontend_api(self) -> FrontendAPI:
        """
        returns the FrontendAPI in singleton design fashion, meaning there is only one instance of FrontendAPI
        in circulation at all times.

        Returns:
            FrontendAPI: singleton FrontendAPI object
        """
        if self.__instance is None:
            exceptionHandler = ExceptionHandler()
            self.__start_api(self)
        else:
            pass

    def __start_api(self):
        # serve(app, host="127.0.0.1", port=5000)
        app.run(debug='true')

    @staticmethod
    @app.route('/')
    def default_get():
        return "Welcome", 200

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
        # hier wird der Server mit ip geholt
        server = ServerData.getServer()
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
            ServerData.writeServer(server)
        except MatFlowException as exception:
            ExceptionHandler.handle_exception(exception.get_status_code())
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
        pass
        # return json

    @staticmethod
    @app.route('/set_user_details', methods=['POST'])
    def set_user_details() -> str:
        """
        sets all user details (user name, privilege, status) for a specific user in a json format.
        If user does not already exist, one will be created.

        Args:
            json_details(String): contains the user details

        Returns:
            String: response indicating successful request
        """
        pass

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
        pass

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
        # return json
        pass

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
        pass

    @staticmethod
    @app.route('/create_version_of_wf_instance', methods=['POST'])
    def create_version_of_wf_instance() -> str:
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
        pass
        # return json

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
        pass

    @staticmethod
    @app.route('/get_all_wf_instances_names_and_config_file_names', methods=['GET'])
    def get_all_wf_instances_names_and_config_files_names() -> str:
        """
        gets all config file and all workflow instances names

        Returns:
            String: json-dumped object containing all workflow instance names and config file names
        """
        pass
        # return json

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
        pass
        # return json

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
        pass

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
        pass

    @staticmethod
    @app.route('/get_all_template_names', methods=['GET'])
    def get_all_template_names() -> str:
        """
        gets all template names that are registered

        Returns:
            String: json-dumped object that contains all template names
        """
        pass
        # return json

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
        pass
        # return json

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
        pass
        # return file


#########################
## The Flask webserver ##
#########################

if __name__ == "__main__":
    a = FrontendAPI.get_frontend_api()
