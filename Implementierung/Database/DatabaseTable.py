from Implementierung.ExceptionPackage import MatFlowException
import mysql.connector


class DatabaseTable:
    __instance = None

    @staticmethod
    def get_instance():
        if DatabaseTable.__instance is None:
            DatabaseTable()
        return DatabaseTable.__instance

    def __init__(self):
        if DatabaseTable.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DatabaseTable.__instance = self
            return

    # TODO vvv
    """maybe outsource to config file? https://overiq.com/mysql-connector-python-101/connecting-to-mysql-using-connector-python/
    db = mysql.connector.connect(
        host='localhost',
        database='world',
        user='root',
        password='12345',
        port='3306'
    )"""

    def get_database_connection(self):
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

    def set(self, create: str) -> None:
        """Set new values into tables in database.

        Throw error if value already exists,
        or if values are in violation with something

        Args:
            create(str): mysql-query for setting new value(s)

        Returns:
            void

        """
        # connect to database
        db = self.get_database_connection()
        cursor = db.cursor()

        try:
            cursor.execute(create)
        except mysql.connector.Error as err:
            raise MatFlowException.InternalException(err.msg)

        # commit changes
        db.commit()
        # disconnect from database
        cursor.close()
        db.close()
        return

    def delete(self, remove_query: str) -> None:
        """Delete rows in a table of the database.

        Do nothing if nothing fit the deletion query.

        Args:
            remove_query(str): mysql-query to delete something

        Returns:
            void

        """
        # connect to database
        db = self.get_database_connection()
        cursor = db.cursor()

        try:
            cursor.execute(remove_query)
        except mysql.connector.Error as err:
            raise MatFlowException.InternalException(err.msg)

        # commit changes
        db.commit()
        # disconnect from database
        cursor.close()
        db.close()
        return

    def modify(self, change: str) -> None:
        """Modify values in database.

        Throw error if query was not able to be read.

        Args:
            change(str): mysql-query to change values

        Returns:
            void

        """
        # connect to database
        db = self.get_database_connection()
        cursor = db.cursor()

        try:
            cursor.execute(change)
        except mysql.connector.Error as err:
            raise MatFlowException.InternalException(err.msg)

        # commit changes
        db.commit()
        # disconnect from database
        cursor.close()
        db.close()
        return

    def get_multiple(self, query: str) -> str:
        """Search for multiple values in database.

        Throw error if no entry found in database.

        Args:
            query(str): mysql-query to get value(s)

        Returns:
            list[str]: answer of the database

        """
        # connect to database
        db = self.get_database_connection()
        cursor = db.cursor()

        try:
            cursor.execute(query)
        except mysql.connector.Error as err:
            raise MatFlowException.InternalException(err.msg)

        data = cursor.fetchall()

        # disconnect from database
        cursor.close()
        db.close()

        return data

    def get_one(self, query: str) -> str:
        """Search for one(1)/first entry in database

        Throw error if no entry found in database.

        Args:
            query(str): mysql-query to get value(s)

        Returns:
            list[str]: answer of the database

        """
        # connect to database
        db = self.get_database_connection()
        cursor = db.cursor()

        try:
            cursor.execute(query)
        except mysql.connector.Error as err:
            raise MatFlowException.InternalException(err.msg)

        data = cursor.fetchone()

        # cursor blocks if not all entries have been fetched
        cursor.fetchall()

        # disconnect from database
        cursor.close()
        db.close()

        return data

    def check_for(self, query: str) -> bool:
        """Check if at least one(1) entry already exists for given SELECT-query.
        True if one entry is found.

        Args:
            query(str): mysql-query to get check

        Returns:
            bool: true if existing value >= 1

        """
        # connect to database
        db = self.get_database_connection()
        cursor = db.cursor()

        try:
            cursor.execute(query)
        except mysql.connector.Error as err:
            raise MatFlowException.InternalException(err.msg)

        data = False
        if cursor.fetchone():
            data = True

        # disconnect from database
        cursor.close()
        db.close()

        return data

    def setup_database(self):
        """first setup of tables in the database.

        Establish connection to Database with set parameters.
        Read queries from external file "Database_Table_Setup.txt" and execute.

        Print error, but don't crash if tables are already up

        """
        # connection to database
        db = self.get_database_connection()
        cursor = db.cursor()

        # queries outsourced to avoid overly long lines in code
        database_setup_file = open("Database_Table_Setup.txt", 'r')
        database_setup = database_setup_file.read().replace("\n", "").split(";")

        # actual queries

        for line in database_setup:
            if line == "":  # end of file
                break

            # avoid error on double execution
            try:
                cursor.execute(line + ";")
                # print("success creation: " +line)           #debugging
            except mysql.connector.Error as err:
                print(err)  # tmp for debugging
                raise MatFlowException.InternalException(err.msg)

        # close connection
        cursor.close()
        db.close()


#

def init_tests():
    print("TEST IN DatabaseTable START")
    print("Comment out if not needed/crashes program because no Databaseconnection could be established")

    d_table = DatabaseTable.get_instance()
    d_table.setup_database()

    print("TEST IN DatabaseTable END!")


def remove(tables):
    """helping function for deleting all tables"""
    d_table = DatabaseTable.get_instance()
    db = d_table.get_database_connection()
    cursor = db.cursor()

    for rem in tables:
        print("Delete Table" + rem)
        tmp = "DROP TABLE {}".format(rem)
        cursor.execute(tmp)
        db.commit()
    cursor.close()
    db.close()


def clear_tables(tables):
    """helping function for clearing all tables"""
    d_table = DatabaseTable.get_instance()
    db = d_table.get_database_connection()
    cursor = db.cursor()

    for rem in tables:
        print("Clear " + rem)
        tmp = "DELETE FROM {}".format(rem)
        cursor.execute(tmp)
        db.commit()
    cursor.close()
    db.close()


table_names = ["VersionFile", "ConfFile", "ResultFile", "ActiveVersion", "Version", "FolderFile", "Workflow",
               "WorkflowTemplate", "Server"]
# init_tests()
clear_tables(table_names)
# remove(table_names)

