import requests
from requests.exceptions import ConnectionError
from airflow.plugins_manager import AirflowPlugin
# workaround as 3rd party modules are not found. However, importing them in local modules
# makes them available somehow. Bug in airflow app


def discover_matflow_port(base_url: str) -> str:
    port = 8080
    port_found = False
    while not port_found:
        try:
            requests.get("http://localhost:" + str(port) + "/#/" + base_url)
        except ConnectionError:
            print("Matflow not on: " + str(port) + ", still searching..")
            port_found = False
            port += 1
        else:
            port_found = True

    return "http://localhost:" + str(port) + "/#/" + base_url


choose_config_file = {
    "name": "ChooseConfigFile",
    "href": discover_matflow_port("ChooseConfigFile")
}

create_template = {
    "name": "CreateTemplate",
    "href": discover_matflow_port("CreateTemplate")
}

create_workflow_instance = {
    "name": "CreateWorkflowInstance",
    "href": discover_matflow_port("CreateWorkflowInstance")
}

log_in = {
    "name": "LogIn",
    "href": discover_matflow_port("LogIn")
}

sign_up = {
    "name": "SignUp",
    "href": discover_matflow_port("SignUp")
}

server_config = {
    "name": "ServerConfig",
    "href": discover_matflow_port("ServerConfig"),
    "category": "Admin"
}

user_administration = {
    "name": "UserAdministration",
    "href": discover_matflow_port("UserAdministration"),
    "category": "Admin"
}

version_control = {
    "name": "VersionControl",
    "href": discover_matflow_port("VersionControl")
}


class MatflowMenuPlugin(AirflowPlugin):
    name = "Matflow Menu Plugin"
    appbuilder_menu_items = [choose_config_file, create_template, create_workflow_instance,
                             log_in, sign_up, server_config, user_administration, version_control]
    print("initializing matflow menu items")

