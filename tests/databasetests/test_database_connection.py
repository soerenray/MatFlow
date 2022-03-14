import os
from pathlib import Path
import mysql.connector
from matflow.database.DatabaseTable import DatabaseTable
import unittest

class TestDatabaseConnection(unittest.TestCase):
    def test_connection(self):
        p = Path(__file__)
        # dir path
        dir_abs = p.parent.absolute()
        path_to_conf = os.path.join(dir_abs, "mydb.conf")
        return mysql.connector.connect(host='localhost',
                                user='matflow_user',
                                password='qMyaU7AjPJ3Epsmc',
                                port=3306)