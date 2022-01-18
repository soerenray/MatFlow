
""" Erinnerung für mich
def func(arg1, arg2):
    ""(")Summary line.

    Extended description of function.

    Args:
        arg1 (int): Description of arg1
        arg2 (str): Description of arg2

    Returns:
        bool: Description of return value

    ""(")
    return True"""

import mysql.connector
class DatabaseData:
    __instance = None

    @staticmethod
    def get_instance():
        if DatabaseData.__instance == None:
            DatabaseData()
        return DatabaseData.__instance

    def __init__(self):
        if DatabaseData.__instance != None:
            #throw exception
        else:
            DatabaseData.__instance = self

"""maybe outsource to config file? https://overiq.com/mysql-connector-python-101/connecting-to-mysql-using-connector-python/
    db = mysql.connector.connect(
        host='localhost',
        database='world',
        user='root',
        password='12345',
        port='3306'
    )"""



    def initialise():
        """Initialisation of Database if not already done beforehand.

        Go through every table that has to be set up in the database."""
        server_Init = "CREATE TABLE Server (ip varchar(50) PRIMARY KEY,name varchar(255) NOT NULL)"
        Workflow_Template_Init = ""
        FolderFile_Init = ""
        Workflow_Init = ""
        Version_Init = ""
        ActiveVersion_Init = ""
        Versionfile_Init = ""
        ConfFile_Init = ""
        ResultFile_Init = ""



        db = mysql.connector.connect(
            host='localhost',
            database='world',
            user='root',
            password='12345',
            port='3306'
        )
        cursor = db.cursor



    def set(create):
        db = mysql.connector.connect(
            host='localhost',
            database='world',
            user='root',
            password='12345',
            port='3306'
        )

        cursor = db.cursor()

        cursor.execute(create)



    def delete(del):

    def modify(change):

    def get(query):


