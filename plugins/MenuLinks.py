from airflow.plugins_manager import AirflowPlugin


def discover_matflow_port(base_url: str) -> str:
    # airflow is on 8080
    port = 8081
    end_address = "http://localhost:" + str(port) + "/" + base_url
    return end_address


choose_config_file = {
    "name": "ChooseConfigFile",
    "href": discover_matflow_port("ChooseConfigFile"),
    "category": "Develop"
}

create_template = {
    "name": "CreateTemplate",
    "href": discover_matflow_port("CreateTemplate"),
    "category": "Develop"
}

create_workflow_instance = {
    "name": "CreateWorkflowInstance",
    "href": discover_matflow_port("CreateWorkflowInstance"),
    "category": "Develop"
}

# matflow login is deprecated
# log_in = {
#    "name": "LogIn",
#    "href": discover_matflow_port("LogIn"),
#    "category": "Authentication"
#}

sign_up = {
    "name": "SignUp",
    "href": discover_matflow_port("SignUp"),
    "category": "Authentication"
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
    "href": discover_matflow_port("VersionControl"),
    "category": "Develop"
}


class MatflowMenuPlugin(AirflowPlugin):
    name = "Matflow Menu Plugin"
    appbuilder_menu_items = [choose_config_file, create_template, create_workflow_instance,
                             sign_up, server_config, user_administration, version_control]

