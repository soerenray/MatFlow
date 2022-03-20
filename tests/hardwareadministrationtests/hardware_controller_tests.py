import unittest
from matflow.hardwareadministration.Server import Server
from matflow.hardwareadministration.Hardware_Controller import Hardware_Controller


class HardwareControllerTest(unittest.TestCase):
    test_server = Server()
    test_hardware_controller = Hardware_Controller()

    @unittest.skip("docker required")
    def test_get_server_with_permission(self):
        self.assertEqual(self.test_server, self.test_hardware_controller.getServer("airflow", "airflow"))

    @unittest.skip("docker required")
    def test_set_server(self):
        test_server2 = Server()
        test_server2.setName("test_server2")
        self.assertEqual(test_server2.getName(), "test_server2")
        self.test_hardware_controller.setServer(test_server2, "airflow", "airflow")

    @unittest.skip("docker required")
    def test_write_server(self):
        self.test_hardware_controller.write_server(self.test_server)
        self.assertEqual(self.test_server, self.test_hardware_controller.get_server())

    if __name__ == "__main__":
        unittest.main()