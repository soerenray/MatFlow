import Path from pathlib

class DatabaseVersion(Version):
    """
    This class inherits from Version and is specialized to fit the way versions are managed in the database
    """
    def __init__(self, version_number: VersionNumber, note: str, changed_config_files: Path):
        """Constructor of class DatabaseVersion.

        Args:
            version_number (VersionNumber): Number that identifies the new Version
            note (str): Note from user that can be used for documenting the version
            changed_config_files (Path): Path to directory containing all changed files
        """
        self.__version_number = version_number
        self.__note = note
        self.__changed_config_files = changed_config_files

    #getter

    def get_changed_config_files(self)-> Path:
        """Gets path to files that were changed compared to the predecessor version.

        Returns:
            Path: Path to files
        """
        return self.__changed_config_files

    #setter

    def set_changed_config_files(self, changed_config_files: Path):
        """Sets new path to files that were changed compared to the predecessor version.

        Args:
            changed_config_files (Path): The new path
        """
        self.__changed_config_files = changed_config_files