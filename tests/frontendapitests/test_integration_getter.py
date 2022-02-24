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
from matflow.exceptionpackage.MatFlowException import InternalException
from matflow.useradministration.User import User


# Docker compose/nomad must have been started
# All fail cases have been caught in unittests. We want to test integrity, so only use cases that
# should work, meaning all use cases that don't throw exceptions
from matflow.workflow.workflow_manager import WorkflowManager


class GetterTest(unittest.TestCase):
    app = app.test_client()

    @classmethod
    def setUpClass(cls) -> None:
        cls.create_wf_instance()
        cls.create_template()

    def tearDown(self) -> None:
        # deletes all folders in temp_in
        dir_path = Path(__file__).parent.parent.parent
        for file in os.listdir(os.path.join(dir_path, "matflow", "frontendapi", "temp_in")):
            for element in os.listdir(os.path.join(dir_path, "matflow", "frontendapi", "temp_in", file)):
                os.remove(os.path.join(dir_path, "matflow", "frontendapi", "temp_in", file, element))
            os.rmdir(os.path.join(dir_path, "matflow", "frontendapi", "temp_in", file))

    @classmethod
    def create_wf_instance(cls):
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


    @classmethod
    def create_template(cls):
        template_name = "test_template"
        dag_name = "daggy.py"
        with open(Path(os.path.join(os.getcwd(), "res", "dag_test.py")), "rb") as file:
            read_file = file.read()
            encoded_dag = base64.b64encode(read_file).decode("utf-8")
        input_dict = {keys.template_name: template_name, keys.dag_definition_name: dag_name,
                      keys.file_key: encoded_dag}
        send_off = json.dumps(input_dict)
        got = json.loads(cls.app.post("create_template", json=send_off).get_data())

    def test_get_all_users(self):
        got = json.loads(self.__class__.app.get("get_all_users_and_details").get_data())
        expected = json.loads(json.dumps({keys.all_users: [{keys.user_name: "airflow",
                                                            keys.user_status_name: True,
                                          keys.user_privilege_name: "Admin"}],
                                          keys.status_code_name: 607}))
        self.assertEqual(expected, got)

    def test_get_server_details(self):
        # TODO test get nachdem Server überschrieben
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

    def test_get_all_wf_instances(self):
        # Fehler bei Query bei Lukas, siehe Slack
        got = self.__class__.app.get("get_all_wf_instances_names_and_config_file_names")
        print(got)

    def test_get_wf_instance_versions_test(self):
        # Fehler bei Lukas, noch nicht implementiert, siehe wf manager 336;
        # get_versions_from_workflow_instance
        input_data = json.dumps({keys.workflow_instance_name: "test_instance"})
        got = json.loads(self.__class__.app.get("get_wf_instance_versions", json=input_data).get_data())
        print(got)

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
        # Fehler bei Connection (Lukas)
        got = json.loads(self.__class__.app.get("get_all_wf_instances_names_and_config_file_names").get_data())
        print(got)

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


if __name__ == "__main__":
    unittest.main()
