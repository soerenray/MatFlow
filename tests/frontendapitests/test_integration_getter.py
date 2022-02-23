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
class GetterTest(unittest.TestCase):
    app = app.test_client()

    def setUpClass(cls) -> None:
        cls.create_wf_instance()

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
        a = cls.app.post("create_workflow_instance", json=send_off)

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

    def test_get_all_wf_instances(self):
        got = self.__class__.app.get("get_all_wf_instances_names_and_config_file_names")
        print(got)

    def test_get_wf_instance_versions_test(self):
        input_data = json.dumps({keys.workflow_instance_name: "test_instance"})
        got = json.loads(self.app.get("get_wf_instance_versions", data=input_data).get_data())
        print(got)


if __name__ == "__main__":
    unittest.main()
