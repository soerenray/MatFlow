import os
from pathlib import Path
from Implementierung.FrontendAPI import utilities

user_status_name: str = "userStatus"
user_privilege_name: str = "userPrivilege"
password_name: str = "password"
repeat_password_name: str = "repeatPassword"
user_name = "userName"

template_name: str = "templateName"
workflow_instance_name: str = "workflowInstanceName"
version_number_name: str = "versionNumber"
version_note_name: str = "versionNote"
config_file_name: str = "configFileName"
versions_name: str = "versions"
key_value_pairs_name: str = "keyValuePairs"

workflow_instance_names: str = "workflowInstanceNames"
config_file_names: str = "configFileNames"
template_names: str = "templateNames"

dag_picture_name: str = "dagPicture"
dag_definition_name: str = "dagDefinitionFile"

status_code_name: str = "statusCode"


server_name: str = "serverName"
selected_for_execution_name: str = "selectedForExecution"
server_resources_name: str = "serverResources"
server_address_name: str = "serverAddress"
server_status_name: str = "serverStatus"
container_limit_name: str = "containerLimit"


temp_in_name: str = "temp_in"
temp_out_name: str = "temp_out"

files_key: str = "file[]"
file_key: str = "file"

config_save_path: str = "config"
dag_save_path: str = "dag_file"

underscore: str = "_"

temp_in_path: str = os.path.join(utilities.parent_path, temp_in_name)

