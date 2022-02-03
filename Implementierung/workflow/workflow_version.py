from Implementierung.workflow.version_number import VersionNumber


class WorkflowVersion:
    """
    This class represents a version of a workflow instance.
    It's main task is to switch between the two different representations of versions one in the frontend,
    one in the database.
    """
    __note: str
    __version_number: VersionNumber

    def __init__(self, version_number: VersionNumber, note: str):
        """Constructor of class Version. Raises internal exception if the argument version_number has wrong format

        Args:
            version_number (VersionNumber): Number that identifies the new Version
            note (str): Note from user that can be used for documenting the version
        """
        self.__version_number = version_number
        self.__note = note

    # getter

    def get_version_number(self) -> VersionNumber:
        """Gets the number of the version.

        Returns:
            VersionNumber: number of the version
        """
        return self.__version_number

    def get_note(self) -> str:
        """Gets the note attached to the version.

        Returns:
            str: Attached note
        """
        return self.__note

    # setter

    def set_version_number(self, version_number: VersionNumber):
        """Sets the number of the version.

        Args:
            version_number (VersionNumber): The new version number of the version
        """
        self.__version_number = version_number

    def set_note(self, note: str):
        """Sets the version note

        Args:
            note (str): The new note
        """
        self.__note = note
