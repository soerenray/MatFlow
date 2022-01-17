from pathlib import Path
from typing import List, Tuple
from workflow.reduced_config_file import ReducedConfigFile


class ConfigFile(ReducedConfigFile):
    """
    This is a subclass of ReducedConfigFile and additionally holds the config-file
    itself as well as the name of the associated workflow instance.
    """
    def __init__(self, file_name: str, key_value_pairs: List[Tuple[str, str]], file: Path):
        """Constructor of class ConfigFile.

        Args:
            file_name (str): The name of the config-file through which the config-file can be identified among other
            config files of the workflow instance
            key_value_pairs (list[tuple[str,str]]): The contents of the file in key-value-pair representation
            file (Path): Specifies the path of the file that is represented by this object
        """
        super().__init__(file_name, key_value_pairs)
        self.__file = file

    # getter

    def get_file(self) -> Path:
        """Gets the path of the config file.

        Returns:
            Path: Path of the config file.
        """
        return self.__file

    # setter

    def set_file(self, file: Path):
        """Sets the path of the config file

        Args:
            file (Path): The new path
        """
        self.__file = file

    # public methods

    def apply_changes(self, updated_file: ReducedConfigFile):
        """Finds differences between self and the given file and writes them to self.file

        The method compares the key-value-pairs given through the ReducedConfigFile to the pairs of the object itself.
        Changes detected are applied to the actual config file that is located in the database.

        Args:
            updated_file (ReducedConfigFile): The updated reduced version of the file
        """
    # private methods

    def __find_changes(self, updated_file: ReducedConfigFile) -> List[Tuple[str, str, str, str]]:
        """
        Compares the key value file
        """
        pass

    def __write_changes_to_file(self, changes: List[Tuple[str, str, str, str]]):
        """
        comment
        """