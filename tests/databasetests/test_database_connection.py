import os
from pathlib import Path
import mysql.connector
from matflow.database.DatabaseTable import DatabaseTable
import unittest


class TestDatabaseConnection(unittest.TestCase):
    def connection(self):
        p = Path(__file__)
        # dir path
        dir_abs = p.parent.absolute()
        path_to_conf = os.path.join(dir_abs, "../../matflow/database/mydb.conf")
        return mysql.connector.connect(option_files=path_to_conf)
