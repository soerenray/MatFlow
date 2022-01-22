from pathlib import Path
from os import listdir
from typing import List, Tuple

from workflow.version import Version
from workflow.version_number import VersionNumber
from workflow.frontend_version import FrontendVersion
from workflow.config_file import ConfigFile
from .parameter_change import ParameterChange
from ExceptionPackage.MatFlowException import InternalException


class DatabaseVersion(Version):
    """
    This class inherits from Version and is specialized to fit the way versions are managed in the database
    """
    __changed_config_files: Path

    def __init__(self, version_number: VersionNumber, note: str, changed_config_files: Path):
        """Constructor of class DatabaseVersion.

        Args:
            version_number (VersionNumber): Number that identifies the new Version
            note (str): Note from user that can be used for documenting the version
            changed_config_files (Path): Path to directory containing all changed files
        """
        super().__init__(version_number, note)
        self.__changed_config_files = changed_config_files

    # getter

    def get_changed_config_files(self) -> Path:
        """Gets path to files that were changed compared to the predecessor version.

        Returns:
            Path: Path to files
        """
        return self.__changed_config_files

    # setter

    def set_changed_config_files(self, changed_config_files: Path):
        """Sets new path to files that were changed compared to the predecessor version.

        Args:
            changed_config_files (Path): The new path
        """
        self.__changed_config_files = changed_config_files

    # public methods
    def get_frontend_version(self, old_config_files: Path) -> FrontendVersion:
        """ Returns the frontend representation of the version.

        Extracts specific parameter changes from changed_config_files by pairwise comparing them to the files of the
        previous version that are expected to be stored at the given path. If the filenames at the given path don't
        match those in changed_config_files an error is thrown.

        Args:
            old_config_files (Path): Path to the files of the previous version

        Returns:
            FrontendVersion: Frontend representation of the version.

        """
        new_files: List[str] = listdir(self.get_changed_config_files())
        old_files: List[str] = listdir(old_config_files)
        # we hope that those lists contain the same elements

        # first check the count of elements in both lists
        if len(new_files) > len(old_files):
            raise InternalException("Internal Error: Too little comparison files for version " +
                                    self.get_version_number().get_number())
        elif len(new_files) < len(old_files):
            raise InternalException("Internal Error: Too many comparison files for version " +
                                    self.get_version_number().get_number())

        # then sort and compare them
        new_files.sort()
        old_files.sort()
        if new_files != old_files:
            raise InternalException("Internal Error: Wrong comparison files for version " +
                                    self.get_version_number().get_number())

        # the file names match now we can start the actual comparison
        parameter_changes: List[ParameterChange] = []  # the distinct changes go in here
        for file in new_files:
            new_path: Path = self.get_changed_config_files() / file
            old_path: Path = old_config_files / file
            new_file: ConfigFile = ConfigFile(file, new_path)
            old_file: ConfigFile = ConfigFile(file, old_path)
            # those are the changes as quadruple (old_key, new_key, old_value, new_value)
            changes: List[Tuple[str, str, str, str]] = old_file.find_changes(new_file)
            # but we want a quintuple with the file name added
            for change in changes:
                parameter_changes.append(ParameterChange(change[0], change[1], change[2], change[3], file))
        return FrontendVersion(self.get_version_number(), self.get_note(), parameter_changes)
