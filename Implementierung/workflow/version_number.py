from typing import List, Pattern
import re
from ExceptionPackage.MatFlowException import InternalException


class VersionNumber:
    """
    This class represents string expressions that are valid version numbers
    """
    __number: str

    def __init__(self, number: str):
        """Translates correct string expressions into VersionNumber objects

        Only works if the expression is correct. Otherwise, throws error.

        Args:
            number (str): The version number
        """
        p: Pattern[str] = re.compile('1(\.[1-9][0-9]*)*')
        if not p.fullmatch(number):
            raise InternalException("Internal Error: " + number + " isn't a valid version number.")
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
        if self.get_number() == "1":
            raise InternalException("Internal Error: Version '1' has no predecessor.")

        # otherwise, the version number has a predecessor
        version_number_components: List[str] = self.get_number().split(".")
        version_number_components.pop(len(version_number_components)-1)  # remove last component of the version number
        point_seperator: str = "."
        predecessor_str: str = point_seperator.join(version_number_components)  # reconnect the components
        return VersionNumber(predecessor_str)

    def get_successor(self, existing_version_numbers: List[str]):
        """
        Builds the smallest subsequent version number that doesn't exist yet.

        Args:
            existing_version_numbers (List[str]): List of all existing version numbers.

        Returns:
            VersionNumber: The new subsequent version number
        """
        successor_postfix: int = 1
        while True:
            possible_successor: str = self.get_number() + "." + str(successor_postfix)
            if not existing_version_numbers.__contains__(possible_successor):
                return VersionNumber(possible_successor)
            successor_postfix += 1  # otherwise, we try the next option

