import os
from pathlib import Path
from typing import List

from matflow.exceptionpackage import MatFlowException
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

    @staticmethod
    def __get_database_connection():
        """Connect to MySQL database and return connection.

        Parameters are set in file mydb.conf."""

        # read from file instead of hard-coding
        # mydb.conf is in same dir
        # current file path
        p = Path(__file__)
        # dir path
        dir_abs = p.parent.absolute()
        path_to_conf = os.path.join(dir_abs, "mydb.conf")
        return mysql.connector.connect(option_files=path_to_conf)

    def set(self, create: str, arguments: tuple) -> None:
        """Set new values into tables in database.

        Args:
            create(str): mysql-query for setting new value(s)
            arguments(tuple): tuple with str values to prevent injections

        Returns:
            void

        """
        # connect to database
        db = self.__get_database_connection()
        cursor = db.cursor()

        try:
            cursor.execute(create, arguments)
        except mysql.connector.Error as err:
            raise MatFlowException.InternalException(err.msg)

        # commit changes
        db.commit()
        # disconnect from database
        cursor.close()
        db.close()
        return

    def delete(self, remove_query: str, arguments: tuple) -> None:
        """Delete rows in a table of the database.

        Do nothing if nothing fit the deletion query.

        Args:
            remove_query(str): mysql-query to delete something
            arguments(tuple): tuple with str values to prevent injections

        Returns:
            void

        """
        # connect to database
        db = self.__get_database_connection()
        cursor = db.cursor()

        try:
            cursor.execute(remove_query, arguments)
        except mysql.connector.Error as err:
            raise MatFlowException.InternalException(err.msg)

        # commit changes
        db.commit()
        # disconnect from database
        cursor.close()
        db.close()
        return

    def modify(self, change: str, arguments: tuple) -> None:
        """Modify values in database.

        Throw error if query was not able to be read.

        Args:
            change(str): mysql-query to change values
            arguments(tuple): tuple with str values to prevent injections

        Returns:
            void

        """
        # connect to database
        db = self.__get_database_connection()
        cursor = db.cursor()

        try:
            cursor.execute(change, arguments)
        except mysql.connector.Error as err:
            raise MatFlowException.InternalException(err.msg)

        # commit changes
        db.commit()
        # disconnect from database
        cursor.close()
        db.close()
        return

    def get_multiple(self, query: str, arguments: tuple) -> List[object]:
        """Search for multiple values in database.

        Throw error if no entry found in database.

        Args:
            query(str): mysql-query to get value(s)
            arguments(tuple): tuple with str values to prevent injections

        Returns:
            list[str]: answer of the database

        """
        # connect to database
        db = self.__get_database_connection()
        cursor = db.cursor()

        try:
            cursor.execute(query, arguments)
        except mysql.connector.Error as err:
            raise MatFlowException.InternalException(err.msg)

        data = cursor.fetchall()

        # disconnect from database
        cursor.close()
        db.close()

        return data

    def get_one(self, query: str, arguments: tuple) -> str:
        """Search for one(1)/first entry in database

        Throw error if no entry found in database.

        Args:
            query(str): mysql-query to get value(s)
            arguments(tuple): tuple with str values to prevent injections

        Returns:
            list[str]: answer of the database

        """
        # connect to database
        db = self.__get_database_connection()
        cursor = db.cursor()

        try:
            cursor.execute(query, arguments)
        except mysql.connector.Error as err:
            raise MatFlowException.InternalException(err.msg)

        data = cursor.fetchone()

        # cursor blocks if not all entries have been fetched
        cursor.fetchall()

        # disconnect from database
        cursor.close()
        db.close()

        return data

    def check_for(self, query: str, arguments: tuple) -> bool:
        """Check if at least one(1) entry already exists for given SELECT-query.
        True if one entry is found.

        Args:
            query(str): mysql-query to get check
            arguments(tuple): tuple with str values to prevent injections

        Returns:
            bool: true if existing value >= 1

        """
        # connect to database
        db = self.__get_database_connection()
        cursor = db.cursor()

        try:
            cursor.execute(query, arguments)
        except mysql.connector.Error as err:
            raise MatFlowException.InternalException(err.msg)

        data = False
        if cursor.fetchone():
            data = True

        # disconnect from database
        cursor.close()
        db.close()

        return data
