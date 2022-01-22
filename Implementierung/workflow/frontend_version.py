from typing import List
from .version import Version
from .version_number import VersionNumber
from .parameter_change import ParameterChange


class FrontendVersion(Version):
    """
    This class inherits from Version and is specialized to satisfy the need for information of the client application.
    """
    def __init__(self, version_number: VersionNumber, note: str, changes: List[ParameterChange]):
        """Constructor of class FrontendVersion.

        Args:
            version_number (VersionNumber): Number that identifies the new Version
            note (str): Note from user that can be used for documenting the version
            changes (list[ParameterChange]): Contains the difference to the predecessor version in form of the
            changed key-value-pairs
        """
        super().__init__(version_number, note)
        self.__changes = changes

    # getter

    def get_changes(self) -> List[ParameterChange]:
        """Gets the parameter changes compared to the predecessor version.

        Returns:
            list[ParameterChange]: List of changes
        """
        return self.__changes

    # setter

    def set_changes(self, changes: List[ParameterChange]):
        """Sets the parameter changes compared to the predecessor version.

        Args:
            changes (list[ParameterChange]): The new list of changes
        """
        self.__changes = changes
