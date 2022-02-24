import base64
import json
import os.path
import resource
import unittest
import socket
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch, Mock
from matflow.frontendapi.api import app, FrontendAPI
from matflow.frontendapi import keys
from matflow.frontendapi import utilities
from matflow.exceptionpackage.MatFlowException import InternalException, UserExistsException
from matflow.useradministration.User import User


# Docker compose/nomad must have been started
# All fail cases have been caught in unittests. We want to test integrity, so only use cases that
# should work, meaning all use cases that don't throw exceptions
# The goal is not to test every aspect (done in unittest, it is to test teh integrity of the software
from matflow.workflow.workflow_manager import WorkflowManager


class IntegrationTest(unittest.TestCase):
    app = app.test_client()

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_create_wf_instance()
        cls.test_create_template()
        cls.test_create_user()


    def tearDown(self) -> None:
        # deletes all folders in temp_in
        dir_path = Path(__file__).parent.parent.parent
        for file in os.listdir(os.path.join(dir_path, "matflow", "frontendapi", "temp_in")):
            for element in os.listdir(os.path.join(dir_path, "matflow", "frontendapi", "temp_in", file)):
                os.remove(os.path.join(dir_path, "matflow", "frontendapi", "temp_in", file, element))
            os.rmdir(os.path.join(dir_path, "matflow", "frontendapi", "temp_in", file))

    @classmethod
    def test_create_user(cls):
        payload = json.dumps({keys.user_name: "first_user", keys.password_name: "default",
                              keys.repeat_password_name: "default"})
        got = json.loads(cls.app.post("register_user", json=payload).get_data())
        print(got)
        assert got == json.loads(json.dumps({keys.status_code_name: 607}))


    @classmethod
    def test_create_wf_instance(cls):
        wf_name = "test_instance"
        template_name = "test_template"
        with open(Path(os.path.join(os.getcwd(), "res", "test1.conf")), "rb") as file:
            read_file = file.read()
            encoded_config = base64.b64encode(read_file)
        input_wf_dict = {keys.workflow_instance_name: wf_name,
                             keys.template_name: template_name,
                             keys.config_files: [{keys.file_key: encoded_config.decode("utf-8"),
                                                  keys.config_file_name: "test1.conf"}]}
        send_off = json.dumps(input_wf_dict)
        got = json.loads(cls.app.post("create_workflow_instance", json=send_off).get_data())
        a = (got == {keys.status_code_name: 602})
        b = (got == {keys.status_code_name: 607})
        assert True == (a or b)
        print(got)


    def test_create_wf_instance_double(self):
        wf_name = "test_instance"
        template_name = "test_template"
        with open(Path(os.path.join(os.getcwd(), "res", "test1.conf")), "rb") as file:
            read_file = file.read()
            encoded_config = base64.b64encode(read_file)
        input_wf_dict = {keys.workflow_instance_name: wf_name,
                             keys.template_name: template_name,
                             keys.config_files: [{keys.file_key: encoded_config.decode("utf-8"),
                                                  keys.config_file_name: "test1.conf"}]}
        send_off = json.dumps(input_wf_dict)
        got = json.loads(self.__class__.app.post("create_workflow_instance", json=send_off).get_data())
        self.assertEqual(got, json.loads(json.dumps({keys.status_code_name: 604})))

    @classmethod
    def test_create_template(cls):
        template_name = "test_template"
        dag_name = "daggy.py"
        with open(Path(os.path.join(os.getcwd(), "res", "dag_test.py")), "rb") as file:
            read_file = file.read()
            encoded_dag = base64.b64encode(read_file).decode("utf-8")
        input_dict = {keys.template_name: template_name, keys.dag_definition_name: dag_name,
                      keys.file_key: encoded_dag}
        send_off = json.dumps(input_dict)
        got = json.loads(cls.app.post("create_template", json=send_off).get_data())
        print(got)
        a = (got == {keys.status_code_name: 604})
        b = (got == {keys.status_code_name: 607})
        assert True == (a or b)

    def test_create_templat_double(self):
        template_name = "test_template"
        dag_name = "daggy.py"
        with open(Path(os.path.join(os.getcwd(), "res", "dag_test.py")), "rb") as file:
            read_file = file.read()
            encoded_dag = base64.b64encode(read_file).decode("utf-8")
        input_dict = {keys.template_name: template_name, keys.dag_definition_name: dag_name,
                      keys.file_key: encoded_dag}
        send_off = json.dumps(input_dict)
        got = json.loads(self.__class__.app.post("create_template", json=send_off).get_data())
        self.assertEqual(got, json.loads(json.dumps({keys.status_code_name: 602})))

    def test_get_all_users(self):
        got = json.loads(self.__class__.app.get("get_all_users_and_details").get_data())
        expected = json.loads(json.dumps({keys.all_users: [{keys.user_name: "airflow",
                                                            keys.user_status_name: True,
                                          keys.user_privilege_name: "Admin"}],
                                          keys.status_code_name: 607}))
        self.assertEqual(expected, got)

    def test_get_server_details(self):
        # default server comparison
        hostname = socket.gethostname()
        self.address = socket.gethostbyname(hostname)
        got = json.loads(self.__class__.app.get("get_server_details").get_data())
        expected = json.loads(json.dumps({keys.server_name: 'server',
                                          keys.server_address_name: str(self.address),
                                          keys.server_status_name: True,
                                          keys.container_limit_name: 20,
                                          keys.selected_for_execution_name: True,
                                          keys.server_resources_name: [str(resource.RLIM_INFINITY),
                                                                       str(resource.RLIMIT_CPU)],
                                          keys.status_code_name: 607}))
        self.assertEqual(expected, got)

    def test_reset_server_details(self):
        hostname = socket.gethostname()
        self.address = socket.gethostbyname(hostname)
        payload = json.dumps({keys.server_name: 'server',
                                         keys.server_address_name: str(self.address),
                                         keys.server_status_name: True,
                                         keys.container_limit_name: 25, #only difference
                                         keys.selected_for_execution_name: True,
                                         keys.server_resources_name: [str(resource.RLIM_INFINITY),
                                                                      str(resource.RLIMIT_CPU)]})
        self.__class__.app.put("set_server_details", json=payload).get_data()
        got = json.loads(self.__class__.app.get("get_server_details").get_data())
        expected = json.loads(payload)
        expected.update({keys.status_code_name: 607})
        expected = json.loads(json.dumps(expected))
        self.assertEqual(expected, got)
        # Clean up server
        payload = json.dumps({keys.server_name: 'server',
                                          keys.server_address_name: str(self.address),
                                          keys.server_status_name: True,
                                          keys.container_limit_name: 20,
                                          keys.selected_for_execution_name: True,
                                          keys.server_resources_name: [str(resource.RLIM_INFINITY),
                                                                       str(resource.RLIMIT_CPU)]})
        self.__class__.app.put("set_server_details", json=payload)


    def test_set_user_details(self):
        payload = json.dumps({keys.user_name: "first_user", keys.user_status_name: True,
                              keys.user_privilege_name: "Public", keys.password_name: "airflow"})
        got = json.loads(self.__class__.app.put("set_user_details", json=payload).get_data())
        self.assertEqual(got, json.loads(json.dumps({keys.status_code_name: 607})))

    def test_set_user_no_user(self):
        payload = json.dumps({keys.user_name: "no_user", keys.user_status_name: True,
                              keys.user_privilege_name: "Public", keys.password_name: "airflow"})
        got = json.loads(self.__class__.app.put("set_user_details", json=payload).get_data())
        self.assertEqual(got, json.loads(json.dumps({keys.status_code_name: 601})))

    def test_delete_user(self):
        payload = json.dumps({keys.user_name: "first_user", keys.password_name: "default",
                              keys.user_privilege_name: "Public", keys.user_status_name: "inactive"})
        got = json.loads(self.__class__.app.delete("delete_user", json=payload).get_data())
        self.assertEqual(got, {keys.status_code_name: 607})
        IntegrationTest.test_create_user()

    def test_login(self):
        payload = json.dumps({keys.user_name: "first_user", keys.password_name: "default"})
        got = json.loads(self.__class__.app.get("verify_login", json=payload).get_data())
        self.assertEqual(got, {keys.status_code_name: 607})


    def test_get_all_wf_instances(self):
        # Fehler bei Query bei Lukas, siehe Slack
        got = json.loads(self.__class__.app.get("get_all_wf_instances_names_and_config_file_names").get_data())
        print(got)
        # TODO Florian fix
        self.assertIn("test_instance", got[keys.workflow_instance_names])

    def test_get_wf_instance_versions_test(self):
        # Fehler bei Lukas, noch nicht implementiert, siehe wf manager 336;
        # get_versions_from_workflow_instance
        input_data = json.dumps({keys.workflow_instance_name: "test_instance"})
        got = json.loads(self.__class__.app.get("get_wf_instance_versions", json=input_data).get_data())
        print(got)
        # TODO testen

    def test_get_config_from_wf_instance(self):
        dir_path = Path(__file__).parent.parent.parent
        # conf_name = os.path.join(dir_path, "matflow", "frontendapi","temp_in", "config_0",
        #                          "test1.conf")
        conf_name = os.path.join("test1.conf")
        print(conf_name)
        input_data = json.dumps({keys.workflow_instance_name: "test_instance",
                                 keys.config_file_name: conf_name})
        # TODO richtigen Config File Namen rausfinden Florian
        got = json.loads(self.__class__.app.get("get_config_from_wf_instance", json=input_data).get_data())
        print(got)
        manager = WorkflowManager.get_instance()
        print(manager.get_names_of_workflows_and_config_files())

    def test_get_all_wf_instances_names_and_config_files_names(self):
        # TODO Florian Pfad cleanup
        got = json.loads(self.__class__.app.get("get_all_wf_instances_names_and_config_file_names").get_data())
        print(got)
        # TODO testen

    def test_get_all_template_names(self):
        got = json.loads(self.__class__.app.get("get_all_template_names").get_data())
        self.assertIn("test_template", got[keys.template_names])

    def test_get_template(self):
        input_data = json.dumps({keys.template_name: "test_template"})
        got = json.loads(self.__class__.app.get("get_template", json=input_data).get_data())
        with open(Path(os.path.join(os.getcwd(), "res", "dag_test.py")), "rb") as file:
            read_file = file.read()
            encoded_dag = base64.b64encode(read_file).decode("utf-8")
        self.assertEqual(got, {keys.status_code_name: 607, keys.template_name: "test_template",
                               keys.file_key: {keys.dag_definition_name:  encoded_dag}})

    def test_create_version(self):
        send_off = json.dumps({keys.workflow_instance_name: "test_instance",
                               keys.version_note_name:"note to self: don't code at 2 am",
                               keys.config_files: [{keys.config_file_name: "test_conf1.conf",
                                                    keys.key_value_pairs_name: [("hello", "world")]}]})

        got = json.loads(self.__class__.app.post("create_version_of_wf_instance", json=send_off).get_data())
        self.assertEqual(got, {keys.status_code_name: 607})

    def create_version(self):
        send_off = json.dumps({keys.workflow_instance_name: "test_instance",
                               keys.version_note_name:"note to self: don't code at 2 am",
                               keys.config_files: [{keys.config_file_name: "test_conf1.conf",
                                                    keys.key_value_pairs_name: [("hello", "world")]}]})

        got = json.loads(self.__class__.app.post("create_version_of_wf_instance", json=send_off).get_data())

    def test_replace_version(self):
        self.create_version()
        # TODO complete

    def test_get_graph_for_temporary_template(self):
        template_name = "test_template_contemporary"
        dag_name = "daggy.py"
        with open(Path(os.path.join(os.getcwd(), "res", "dag_test.py")), "rb") as file:
            read_file = file.read()
            encoded_dag = base64.b64encode(read_file).decode("utf-8")
        input_dict = {keys.template_name: template_name, keys.dag_definition_name: dag_name,
                      keys.file_key: encoded_dag}
        send_off = json.dumps(input_dict)
        self.__class__.app.get("get_graph_for_temporary_template", json=send_off)
        self.assertEqual(True, os.path.isfile("workflow/workflowtests/dummy_dag.png"))

# TODO replace active version
if __name__ == "__main__":
    unittest.main()
