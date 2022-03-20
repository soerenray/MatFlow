import unittest
from unittest.mock import patch, Mock


from matflow.database.DatabaseTable import DatabaseTable
from matflow.database.ServerData import ServerData
from matflow.hardwareadministration.Server import Server


class TestServerDataSetup(unittest.TestCase):
    server_data: ServerData
    test_server1: Server
    name1 = "name1"
    ip1 = "173.234.0.9"  # randomly chosen numbers
    status1 = "standby"
    test_server2: Server
    name2 = "way longer name than name 1"
    ip2 = "125.125.125.125"
    status2 = "deactivated"

    def setUp(self) -> None:
        self.server_data = ServerData.get_instance()

        self.test_server1 = Server()
        self.test_server1.setName(self.name1)
        self.test_server1.setAddress(self.ip1)
        self.test_server1.setStatus(self.status1)

        self.test_server2 = Server()
        self.test_server2.setName(self.name2)
        self.test_server2.setAddress(self.ip2)
        self.test_server2.setStatus(self.status2)


class TestServerData(TestServerDataSetup):
    mock_database_table: Mock

    def test_get_instance(self):
        # Test for true singleton
        with patch.object(
            DatabaseTable,
            "get_instance",
            return_value=None,
        ) as mock_get_instance:
            self.assertEqual(self.server_data, ServerData.get_instance())
            self.assertEqual(self.server_data, ServerData.get_instance())

    def test_write_server1(self):
        # Arrange
        with patch.object(DatabaseTable, "set") as database_table_patch:

            # Act
            self.server_data.write_server(self.test_server1)

            # Assert
            database_table_patch.assert_called_once()
            args = str(database_table_patch.call_args)
            self.assertIn("INSERT INTO", args)
            # Only name and address are saved in database
            self.assertIn(self.name1, args)
            self.assertIn(self.ip1, args)

    def test_write_server2(self):
        # Arrange
        with patch.object(DatabaseTable, "set") as database_table_patch:

            # Act
            self.server_data.write_server(self.test_server2)

            # Assert
            database_table_patch.assert_called_once()
            args = str(database_table_patch.call_args)
            # Only name and address are saved in database
            self.assertIn(self.name2, args)
            self.assertIn(self.ip2, args)

    def test_get_server1(self):
        # Arrange
        database_return_value = [(self.ip1, self.name1)]
        with patch.object(
            DatabaseTable, "get_multiple", return_value=database_return_value
        ) as get_multiple_patch:

            # Act
            return_param = self.server_data.get_server()

            # Assert
            get_multiple_patch.assert_called_once()
            self.assertEqual(database_return_value, return_param)

    def test_get_server2(self):
        # Arrange
        database_return_value = [(self.ip1, self.name1), (self.ip2, self.name2)]
        with patch.object(
            DatabaseTable, "get_multiple", return_value=database_return_value
        ) as get_multiple_patch:

            # Act
            return_param = self.server_data.get_server()

            # Assert
            get_multiple_patch.assert_called_once()
            for (ip, name) in return_param:
                if ip == self.ip2:
                    self.assertEqual(self.name2, name)
                elif ip == self.ip1:
                    self.assertEqual(self.name1, name)
                else:
                    self.assertEqual(True, False)


if __name__ == "__main__":
    unittest.main()
