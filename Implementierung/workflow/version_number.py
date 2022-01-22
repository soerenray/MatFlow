from typing import List
import re


class VersionNumber:
    """
    This class represents string expressions that are valid version numbers
    """
    def __init__(self, number: str):
        """Translates correct string expressions into VersionNumber objects

        Only works if the expression is correct. Otherwise, throws error.

        Args:
            number (str): The version number
        """
        p = re.compile('1([.([1-9][0-9]*])*')
        if not p.match(number):
            raise Exception("Internal Error: " + number + " isn't a valid version number.")
        self.__number = number

    # getter

    def get_number(self) -> str:
        """Gets the version number stored in this object.

        Returns:
            str: Version number
        """
        return self.__number

    # setter

    def set_number(self, number: str):
        """Sets the number attribute of the object.

        Args:
            number (str): The new number that has to be a correct version number
        """
        self.__number = number

    # methods

    def get_predecessor(self):
        """
        Just cuts of the postfix ".<int>" from the number of self and puts that str into a new VersionNumber object.
        Raises exception if the current version is version 1.

        Returns:
            VersionNumber: The predecessor version number
        """
    def get_successor(self, existing_version_numbers: List[str]):
        """
        Builds the smallest subsequent version number that doesn't exist yet.

        Args:
            existing_version_numbers (List[str]): List of all existing version numbers.

        Returns:
            VersionNumber: The new subsequent version number
        """