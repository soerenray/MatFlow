from typing import List
from Implementierung.FrontendAPI import keys
from Implementierung.FrontendAPI.ExceptionHandler import ExceptionHandler
from Implementierung.workflow.workflow_version import WorkflowVersion
from Implementierung.workflow.version_number import VersionNumber
from Implementierung.workflow.parameter_change import ParameterChange


class FrontendVersion(WorkflowVersion):
    """
    This class inherits from Version and is specialized to satisfy the need for information of the client application.
    """

    __changes: List[ParameterChange]

    def __init__(
        self, version_number: VersionNumber, note: str, changes: List[ParameterChange]
    ):
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

    def encode_version(self) -> dict:
        """
        encodes all version attributes and dumps them into one json object

        Returns:
            String: json-dumped object containing encoded versions
        """
        out_dict: dict = dict()
        out_dict.update({keys.version_note_name: self.get_note()})
        out_dict.update(
            {keys.version_number_name: self.get_version_number().get_number()}
        )
        changes_list: List[dict] = []
        for change in self.get_changes():
            changes_list.append(change.encode())
        out_dict.update({keys.frontend_versions_changes: changes_list})
        return out_dict
