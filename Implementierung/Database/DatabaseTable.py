import mysql.connector

class DatabaseTable:
    __instance = None

    @staticmethod
    def get_instance():
        if DatabaseTable.__instance == None:
            DatabaseTable()
        return DatabaseTable.__instance

    def __init__(self):
        if DatabaseTable.__instance != None:
            return #throw exception
        else:
            DatabaseTable.__instance = self
            return

    """maybe outsource to config file? https://overiq.com/mysql-connector-python-101/connecting-to-mysql-using-connector-python/
    db = mysql.connector.connect(
        host='localhost',
        database='world',
        user='root',
        password='12345',
        port='3306'
    )"""


    def get_Database_Connection(self):
        """Connect to MySQL Database and return connection.

        Parameters are set."""


        db = mysql.connector.connect(
            host='localhost',
            database='databaseshema',
            user='root',
            password='12345',
            port='3306'
        )
        return db



    def set(self, create):
        """Set new values into tables in database.

        Throw error if value already exists,
        or if values are in violation with something

        Args:
            create(str): mysql-query for setting new value(s)

        Returns:
            void

        """
        db = mysql.connector.connect(
            host='localhost',
            database='databaseshema',
            user='root',
            password='12345',
            port='3306'
        )

        cursor = db.cursor()

        cursor.execute(create)

    def delete(self, remove):
        """Delete rows in a table of the database.

        Do nothing if nothing fit the deletion query.

        Args:
            remove(str): mysql-query to delete something

        Returns:
            void

        """


    def modify(self, change):
        """Modify values in database.

        Throw error if query was not able to be read.

        Args:
            change(str): mysql-query to change values

        Returns:
            void

        """


    def get(self, query):
        """Search for value(s) in database.

        Throw error if no entry found in database.

        Args:
            query(str): mysql-query to get value(s)

        Returns:
            str: answer of the database

        """


    def setup_Database(self):
        """first setup of tables in the database.

        Establish connection to Database with set parameters.
        Read queries from external file "Database_Table_Setup.txt" and execute.

        Print error, but don't crash if tables are already up
        """
        #connection to database
        db = self.get_Database_Connection()
        cursor = db.cursor()

        #queries outsourced to avoid overly long lines in code
        databaseSetupFile = open("Database_Table_Setup.txt", 'r')
        databaseSetup = databaseSetupFile.read().replace("\n", "").split(";")

        # actual queries

        for line in databaseSetup:
            if line == "":  # end of file
                break

            # avoid error on double execution
            try:
                cursor.execute(line + ";")
                # print("success creation: " +line)           #debugging
            except mysql.connector.Error as err:
                print(err)

        #close connection
        cursor.close()
        db.close()

#

print("TEST IN DatabaseTable. Comment out if not neede/crahses program because no Databaseconnection could be established")


dTable = DatabaseTable()
dTable.setup_Database()









print("End of DatabaseTable output check!")
