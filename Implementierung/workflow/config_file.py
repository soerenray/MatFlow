from pathlib import Path
from typing import List, Tuple
from workflow.reduced_config_file import ReducedConfigFile


class ConfigFile(ReducedConfigFile):
    """
    This is a subclass of ReducedConfigFile and additionally holds the config-file
    itself as well as the name of the associated workflow instance.
    """
    def __init__(self, file_name: str, file: Path):
        """Constructor of class ConfigFile.

        The parameter key_value_pairs for the superclass constructor isn't explicitly asked for but rather extracted
        from the given file

        Args:
            file_name (str): The name of the config-file through which the config-file can be identified among other
            config files of the workflow instance
            file (Path): Specifies the path of the file that is represented by this object
        """
        self.__file = file
        super().__init__(file_name, self.__extract_key_value_pairs_from_file())

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
        """Finds differences between self and the given file and writes them to self.file.

        The method compares the key-value-pairs given through the ReducedConfigFile to the pairs of the object itself.
        Changes detected are applied to the actual config file that is located in the database.

        Args:
            updated_file (ReducedConfigFile): The updated reduced version of the file
        """
    # private methods

    def __extract_key_value_pairs_from_file(self) -> List[Tuple[str, str]]:
        """
        Searches for lines that fit the expression "<key> = <value>;" inside the given file.
        If such a line is found (key, value) is added to the result list.
        The method is used to initialize the attribute self.key_value_pairs.
        """
        result = []
        with self.__file.open() as file:
            lines = file.readlines()
            for line in lines:
                if line[0] != '#':  # otherwise, line is comment
                    words = line.split(' ')
                    if len(words) >= 3 and words[1] == "=":  # the general expression is met
                        key = words[0]
                        value_semicolon = words[2]
                        if len(value_semicolon) >= 2 and value_semicolon.__contains__(";"):  # pair is terminated by ';'
                            value = value_semicolon.split(";")[0]  # only str before ';' is of interest
                            result.append((key, value))

        return result

    def __find_changes(self, updated_file: ReducedConfigFile) -> List[Tuple[str, str, str, str]]:
        """
        Compares the key value file
        """
        pass

    def __write_changes_to_file(self, changes: List[Tuple[str, str, str, str]]):
        """
        comment
        """