import unittest
from unittest.mock import patch, Mock

from matflow.database.DatabaseTable import DatabaseTable
from matflow.database.ServerData import ServerData
from matflow.hardwareadministration.Server import Server


class TestServerData(unittest.TestCase):
    mock_database_table: Mock
    server_data: ServerData
    test_server: Server

    def setUp(self) -> None:
        self.server_data = ServerData.get_instance()
        self.test_server = Server()
        self.test_server.setName("name1")
        self.test_server.setAddress("ip example")
        self.test_server.setStatus("standby")

    def test_write_server(self):
        with patch.object(DatabaseTable, "set") as database_table_patch:
            # Arrange
            # Assume that Server() is correct
            self.server_data.write_server(self.test_server)

            database_table_patch.assert_called_once()

    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == "__main__":
    unittest.main()
