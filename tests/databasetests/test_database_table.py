from unittest import TestCase
from unittest.mock import patch, Mock

import mysql.connector
from matflow.database.DatabaseTable import DatabaseTable
from matflow.exceptionpackage import MatFlowException


# TODO too complicated for first use of unittests. Come back to this after writing tests for other classes in module Database
class TestDatabaseTable(TestCase):
    database_table: DatabaseTable
    mysql: Mock

    # names of database tables for teardown
    # with respect to dependencies
    table_names = [
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

    def setUp(self):
        # mock mysql
        self.mysql = Mock()
        # set up Database
        self.database_table = DatabaseTable.get_instance()

    def tearDown(self):
        print("teardown")
        # delete all database tables
        # db = mysql.connector.connect(option_files="../mydb.conf")
        # cursor = db.cursor()
        # for rem in self.table_names:
        #    tmp = "DROP TABLE {}".format(rem)
        #    cursor.execute(tmp)
        #    db.commit()
        # cursor.close()
        # db.close()


class TestConnection(TestDatabaseTable):
    def test_set_get_one(self):
        # because some tables have dependencies and tests are generally not in order
        # all basic table connection test are in this test function

        # Arrange
        workflow_set_query = "INSERT INTO Workflow (name, dag) VALUES (%s, %s)"
        workflow_get_query = "SELECT * FROM Workflow;"

        # Act
        self.database_table.set(workflow_set_query, ("testname1", "testdag1"))

        self.mysql.connector.connect.assert_called()
