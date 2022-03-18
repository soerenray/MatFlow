import base64
import json
import os.path
import resource
import shutil
import unittest
import socket
from pathlib import Path
from typing import List, Tuple

from flask.testing import FlaskClient

from matflow.frontendapi.api import app
from matflow.frontendapi.api import FrontendAPI
from matflow.frontendapi import keys, utilities
import matflow.database.DatabaseTable

# Docker compose/nomad must have been started
# All fail cases have been caught in unittests. We want to test integrity, so only use cases that
# should work, meaning all use cases that don't throw exceptions
# The goal is not to test every aspect (done in unittest, it is to test teh integrity of the software
from matflow.useradministration.UserController import UserController
from matflow.workflow.workflow_manager import WorkflowManager

AUTH = {"username": "airflow", "password": "airflow"}


class IntegrationTest(unittest.TestCase):
    app = app.test_client()

    # @classmethod
    def setUp(self) -> None:
        self.app = app.test_client()
        create_user(self.app, "first_user")
        create_template(
            self.app,
            "test_template",
            "daggy.py",
            Path(__file__).parent / "res" / "dag_test.py",
        )
        create_wf_instance(
            self.app,
            "test_instance",
            "test_template",
            Path(__file__).parent / "res" / "conf_folder_test1",
        )
        note: str = "note to self: don't code at 2 am"
        config_files: List[dict] = [
            {
                keys.config_file_name: "test1.conf",
                keys.key_value_pairs_name: [
                    ("i_was", "replaced"),
                    ("this_one", "as_well"),
                    ("four", "4"),
                    ("also", "find_me"),
                ],
            }
        ]
        create_wf_version(self.app, "test_instance", note, config_files)

    def tearDown(self) -> None:
        tear_down(self.app)

    def test_create_wf_instance_double(self):
        # Arrange
        wf_name = "test_instance"
        template_name = "test_template"
        conf_path: Path = Path(__file__).parent / "res" / "conf_folder_test1"

        # Act
        # this wf_instance was already created in the setup
        got = create_wf_instance(self.app, wf_name, template_name, conf_path)

        # Assert
        expected_status: int = 604  # double wf instance exception
        self.assertEqual(expected_status, dict(got)[keys.status_code_name])

    def test_create_template_double(self):
        # Arrange
        template_name = "test_template"
        dag_name = "daggy.py"
        dag_path = Path(__file__).parent / "res" / "dag_test.py"

        # Act
        # this template was already created in the setup
        got = create_template(self.app, template_name, dag_name, dag_path)

        # Assert
        expected_status: int = 602  # double template exception
        self.assertEqual(expected_status, dict(got)[keys.status_code_name])

    # TODO scheitert ziemlich sicher daran, dass alle User als Admins created werden user_roles != userPriveleges
    def test_get_all_users(self):
        got = json.loads(self.__class__.app.get("get_all_users_and_details", headers=AUTH).get_data())
        print(got)
        expected = json.loads(
            json.dumps(
                {
                    keys.all_users: [
                        {
                            keys.user_name: "airflow",
                            keys.user_status_name: True,
                            keys.user_privilege_name: "Admin",
                        },
                        {
                            keys.user_name: "first_user",
                            keys.user_status_name: True,
                            keys.user_privilege_name: "Admin",
                        },
                    ],
                    keys.status_code_name: 607,
                }
            )
        )
        self.assertEqual(expected, got)

    def test_get_server_details(self):
        # default server comparison
        hostname = socket.gethostname()
        self.address = socket.gethostbyname(hostname)
        got = json.loads(self.__class__.app.get("get_server_details", headers=AUTH).get_data())
        expected = json.loads(
            json.dumps(
                {
                    keys.server_name: "server",
                    keys.server_address_name: str(self.address),
                    keys.server_status_name: True,
                    keys.container_limit_name: 20,
                    keys.selected_for_execution_name: True,
                    keys.server_resources_name: [
                        str(resource.RLIM_INFINITY),
                        str(resource.RLIMIT_CPU),
                    ],
                    keys.status_code_name: 607,
                }
            )
        )
        self.assertEqual(expected, got)

    def test_reset_server_details(self):
        hostname = socket.gethostname()
        self.address = socket.gethostbyname(hostname)
        payload = json.dumps(
            {
                keys.server_name: "server",
                keys.server_address_name: str(self.address),
                keys.server_status_name: True,
                keys.container_limit_name: 25,  # only difference
                keys.selected_for_execution_name: True,
                keys.server_resources_name: [
                    str(resource.RLIM_INFINITY),
                    str(resource.RLIMIT_CPU),
                ],
            }
        )
        self.__class__.app.put("set_server_details", json=payload, headers=AUTH).get_data()
        got = json.loads(self.__class__.app.get("get_server_details").get_data())
        expected = json.loads(payload)
        expected.update({keys.status_code_name: 607})
        expected = json.loads(json.dumps(expected))
        self.assertEqual(expected, got)
        # Clean up server
        payload = json.dumps(
            {
                keys.server_name: "server",
                keys.server_address_name: str(self.address),
                keys.server_status_name: True,
                keys.container_limit_name: 20,
                keys.selected_for_execution_name: True,
                keys.server_resources_name: [
                    str(resource.RLIM_INFINITY),
                    str(resource.RLIMIT_CPU),
                ],
            }
        )
        self.__class__.app.put("set_server_details", json=payload)

    def test_set_user_details(self):
        payload = json.dumps(
            {
                keys.user_name: "first_user",
                keys.user_status_name: True,
                keys.user_privilege_name: "Admin",
                keys.password_name: "airflow",
            }
        )
        got = json.loads(
            self.__class__.app.put("set_user_details", json=payload, headers=AUTH).get_data()
        )
        self.assertEqual(got, json.loads(json.dumps({keys.status_code_name: 607})))

    def test_set_user_no_user(self):
        payload = json.dumps(
            {
                keys.user_name: "no_user",
                keys.user_status_name: True,
                keys.user_privilege_name: "Public",
                keys.password_name: "airflow",
            }
        )
        got = json.loads(
            self.__class__.app.put("set_user_details", json=payload, headers=AUTH).get_data()
        )
        expected_status: int = 601
        self.assertEqual(dict(got)[keys.status_code_name], expected_status)

    def test_delete_user(self):
        payload = json.dumps(
            {
                keys.user_name: "first_user",
                keys.password_name: "default",
                keys.user_privilege_name: "Public",
                keys.user_status_name: True,
            }
        )
        got = json.loads(
            self.__class__.app.delete("delete_user", json=payload, headers=AUTH).get_data()
        )
        self.assertEqual(got, {keys.status_code_name: 607})
        all = json.loads(self.__class__.app.get("get_all_users_and_details").get_data())
        self.assertNotIn(
            {
                keys.user_name: "first_user",
                keys.user_status_name: True,
                keys.user_privilege_name: "Public",
            },
            all[keys.all_users],
        )

    @unittest.skip("no support in api")
    def test_login(self):
        payload = json.dumps(
            {keys.user_name: "first_user", keys.password_name: "default"}
        )
        got = json.loads(
            self.__class__.app.get("verify_login", json=payload).get_data()
        )
        self.assertEqual(got, {keys.status_code_name: 607})

    # same as "test_get_all_wf_instances_names_and_config_files_names"
    def test_get_all_wf_instances(self):
        got = json.loads(
            self.__class__.app.get(
                "get_all_wf_instances_names_and_config_file_names"
            ).get_data()
        )
        print(got)
        self.assertIn("test_instance", got[keys.names_and_configs])

    def test_get_wf_instance_versions_test(self):
        input_data = json.dumps({keys.workflow_instance_name: "test_instance"})
        got = json.loads(
            self.__class__.app.post(
                "get_wf_instance_versions", json=input_data
            ).get_data()
        )
        print(got)
        expected_status: int = 607  # success
        self.assertEqual(expected_status, dict(got)[keys.status_code_name])

    def test_get_config_from_wf_instance(self):
        # Arrange
        conf_name = os.path.join("test1.conf")
        input_data = json.dumps(
            {
                keys.workflow_instance_name: "test_instance",
                keys.config_file_name: conf_name,
            }
        )

        # Act
        got = json.loads(
            self.__class__.app.get(
                "get_config_from_wf_instance", json=input_data, headers=AUTH
            ).get_data()
        )

        # Assert
        expected_status: int = 607
        self.assertEqual(expected_status, dict(got)[keys.status_code_name])
        expected_pairs: List[List[str, str]] = [
            ["find", "this_pair"],
            ["this_one", "as_well"],
            ["three", "3"],
            ["also", "find_me"],
        ]
        self.assertEqual(expected_pairs, dict(got)[keys.key_value_pairs_name])

    def test_get_all_wf_instances_names_and_config_files_names(self):
        # TODO Lukas
        # error in "get_names_of_workflows_and_config_files()" of WorkflowData.py
        # get duplicate file names if there is more than one version
        got = json.loads(
            self.__class__.app.get(
                "get_all_wf_instances_names_and_config_file_names"
            ).get_data()
        )
        expected_status: int = 607
        self.assertEqual(expected_status, dict(got)[keys.status_code_name])
        expected_dict: dict = {"test_instance": ["test1.conf"]}
        self.assertEqual(expected_dict, dict(got)[keys.names_and_configs])
        print(got)

    def test_get_all_template_names(self):
        got = json.loads(self.__class__.app.get("get_all_template_names").get_data())
        self.assertIn("test_template", got[keys.template_names])

    def test_get_template(self):
        # Arrange
        input_data = json.dumps({keys.template_name: "test_template"})
        with open(Path(__file__).parent / "res" / "dag_test.py", "rb") as file:
            read_file = file.read()
            encoded_dag = base64.b64encode(read_file).decode("utf-8")

        # Act
        got = json.loads(
            self.__class__.app.get("get_template", json=input_data).get_data()
        )

        # Assert
        self.assertEqual(
            got,
            {
                keys.status_code_name: 607,
                keys.template_name: "test_template",
                keys.file_key: {keys.dag_definition_name: encoded_dag},
            },
        )

    def test_replace_version(self):
        # TODO Florian: Add workflows to Airflow
        payload: dict = {
            keys.workflow_instance_name: "test_instance",
            keys.version_number_name: "1.1",
        }
        got = json.loads(
            self.__class__.app.put(
                "replace_wf_instance_active_version", json=json.dumps(payload)
            ).get_data()
        )
        self.assertEqual(got, {keys.status_code_name: 607})

    def test_get_graph_for_temporary_template(self):
        template_name = "test_template_contemporary_14"
        dag_name = "daggy.py"
        with open(Path(__file__).parent / "res" / "dag_test.py", "rb") as file:
            read_file = file.read()
            encoded_dag = base64.b64encode(read_file).decode("utf-8")
        input_dict = {
            keys.template_name: template_name,
            keys.dag_definition_name: dag_name,
            keys.file_key: encoded_dag,
        }
        send_off = json.dumps(input_dict)
        got = json.loads(
            self.__class__.app.get(
                "get_graph_for_temporary_template", json=send_off
            ).get_data()
        )
        self.assertEqual(
            got,
            {
                "dagPicture": "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",
                "statusCode": 607,
            },
        )

    def test_tear_down(self):
        self.assertEqual(True, True)


class SetUpTester(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()

    def tearDown(self) -> None:
        tear_down(self.app)

    def test_create_user(self):
        user_name: str = "first_user"
        got: str = create_user(self.app, user_name)
        print(got)
        # actually it should always be a
        a = got == {keys.status_code_name: 607}
        b = got == {keys.status_code_name: 601}
        result = a or b
        self.assertEqual(True, result)

    def test_create_wf_instance(self):
        # Arrange
        # create a template first
        template_name: str = "test_template"
        dag_name: str = "daggy.py"
        dag_path: Path = Path(__file__).parent / "res" / "dag_test.py"
        create_template(self.app, template_name, dag_name, dag_path)

        # prepare instance
        wf_name = "test_instance"
        conf_path: Path = Path(__file__).parent / "res" / "conf_folder_test1"

        # Act
        got = create_wf_instance(self.app, wf_name, template_name, conf_path)

        # Assert
        expected_status: int = 607
        self.assertEqual(expected_status, dict(got)[keys.status_code_name])

    def test_create_template(self):
        # Arrange
        template_name: str = "test_template"
        dag_name: str = "daggy.py"
        dag_path: Path = Path(__file__).parent / "res" / "dag_test.py"

        # Act
        got = create_template(self.app, template_name, dag_name, dag_path)

        # Assert
        expected_status: int = 607
        self.assertEqual(expected_status, dict(got)[keys.status_code_name])

    def test_create_version(self):
        # Arrange
        # create a template first
        template_name: str = "test_template"
        dag_name: str = "daggy.py"
        dag_path: Path = Path(__file__).parent / "res" / "dag_test.py"
        create_template(self.app, template_name, dag_name, dag_path)

        # then create an instance
        instance_name: str = "test_instance"
        conf_path: Path = Path(__file__).parent / "res" / "conf_folder_test1"
        create_wf_instance(self.app, instance_name, template_name, conf_path)

        # finally, prepare the new version
        note: str = "note to self: don't code at 2 am"
        config_files: List[dict] = [
            {
                keys.config_file_name: "test1.conf",
                keys.key_value_pairs_name: [
                    ("i_was", "replaced"),
                    ("this_one", "as_well"),
                    ("four", "4"),
                    ("also", "find_me"),
                ],
            }
        ]

        # Act
        got = create_wf_version(self.app, instance_name, note, config_files)

        # Assert
        expected_status: int = 607
        self.assertEqual(expected_status, dict(got)[keys.status_code_name])


# utility method
def delete_dir_content(dir_path: Path):
    for content in os.listdir(dir_path):
        content_path: Path = dir_path / content
        if os.path.isfile(content_path) or os.path.islink(content_path):
            os.unlink(content_path)
        elif os.path.isdir(content_path):
            shutil.rmtree(content_path)


def create_user(client: FlaskClient, name: str) -> str:
    payload = json.dumps(
        {
            keys.user_name: name,
            keys.password_name: "default",
            keys.repeat_password_name: "default",
        }
    )
    return json.loads(client.post("register_user", json=payload, headers=AUTH).get_data())


def create_template(
    client: FlaskClient, name: str, dag_name: str, file_path: Path
) -> str:
    with open(file_path, "rb") as file:
        read_file = file.read()
        encoded_dag = base64.b64encode(read_file).decode("utf-8")
    input_dict = {
        keys.template_name: name,
        keys.dag_definition_name: dag_name,
        keys.file_key: encoded_dag,
    }
    send_off = json.dumps(input_dict)
    return json.loads(client.post("create_template", json=send_off).get_data())


def create_wf_instance(
    client: FlaskClient, name: str, template_name: str, conf_path: Path
) -> str:
    all_configs_encoded: List[dict] = []
    for file_name in os.listdir(conf_path):
        with open(conf_path / file_name, "rb") as file:
            read_file = file.read()
            encoded_config = base64.b64encode(read_file)
            all_configs_encoded.append(
                {
                    keys.file_key: encoded_config.decode("utf-8"),
                    keys.config_file_name: file_name,
                }
            )
    input_wf_dict = {
        keys.workflow_instance_name: name,
        keys.template_name: template_name,
        keys.config_files: all_configs_encoded,
    }
    send_off = json.dumps(input_wf_dict)
    return json.loads(client.post("create_workflow_instance", json=send_off).get_data())


def create_wf_version(
    client: FlaskClient, instance_name: str, note: str, config_files: List[dict]
) -> str:
    send_off = json.dumps(
        {
            keys.workflow_instance_name: instance_name,
            keys.version_note_name: note,
            keys.config_files: config_files,
        }
    )
    return json.loads(
        client.post("create_version_of_wf_instance", json=send_off).get_data()
    )


def tear_down(client: FlaskClient):
    # shared tear down method from both test cases
    # deletes all folders in temp_in
    dir_path: Path = Path(__file__).parent.parent.parent
    path_to_temp_in: Path = dir_path / "matflow" / "frontendapi" / "temp_in"
    delete_dir_content(path_to_temp_in)

    # also reset the template and wf_instance folders
    wf_instances_path = dir_path / "matflow" / "workflow" / "wf_instances"
    delete_dir_content(wf_instances_path)
    templates_path = dir_path / "matflow" / "workflow" / "templates"
    delete_dir_content(templates_path)

    # reset all tables in database
    table_names: List[str] = [
        "VersionFile",
        "ConfFile",
        "ResultFile",
        "ActiveVersion",
        "Version",
        "FolderFile",
        "Workflow",
        "WorkflowTemplate",
        "Server",
    ]
    matflow.database.DatabaseTable.clear_tables(table_names)

    # delete all users
    user_controller: UserController = UserController()
    user_controller.deleteAllUsers(("airflow", "airflow"))


if __name__ == "__main__":
    unittest.main()
