from pathlib import Path
from typing import List, Tuple, TextIO
from Implementierung.workflow.reduced_config_file import ReducedConfigFile
from Implementierung.ExceptionPackage.MatFlowException import InternalException


class ConfigFile(ReducedConfigFile):
    """
    This is a subclass of ReducedConfigFile and additionally holds the config-file
    itself as well as the name of the associated workflow instance.
    """

    __file: Path

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
        if self.get_file_name() != updated_file.get_file_name():
            # for some reason file name and update name don't match
            raise InternalException(
                "Internal Error: Names of the file: "
                + self.get_file_name()
                + " and the update: "
                + updated_file.get_file_name()
                + " don't match."
            )
        else:  # if the names match we can apply the changes
            changes: List[Tuple[str, str, str, str]] = self.find_changes(updated_file)
            self.__write_changes_to_file(changes)

    def find_changes(
        self, updated_file: ReducedConfigFile
    ) -> List[Tuple[str, str, str, str]]:
        """
        Compares the key-value-pairs of a given ReducedConfig file to those of self. That means the first given pair is
        compared to the first pair of the self, both second pairs are compared and so on. Pairs of pairs that don't
        match up are returned in a list of format (old_key, new_key, old_value, new_value)
        If the lists are of different length an internal exception is thrown.
        """
        if len(self.get_key_value_pairs()) == len(updated_file.get_key_value_pairs()):
            result: List[Tuple[str, str, str, str]] = []
            for old_pair, new_pair in zip(
                self.get_key_value_pairs(), updated_file.get_key_value_pairs()
            ):
                if old_pair != new_pair:  # otherwise, there is no change
                    result.append((old_pair[0], new_pair[0], old_pair[1], new_pair[1]))
            return result
        else:
            raise InternalException(
                "Internal Error: Wrong amount of update-pairs in "
                + self.get_file_name()
            )

    # private methods

    def __extract_key_value_pairs_from_file(self) -> List[Tuple[str, str]]:
        """
        Searches for lines that fit the expression "<key> = <value>;" inside the given file.
        If such a line is found (key, value) is added to the result list.
        The method is used to initialize the attribute self.key_value_pairs.
        """
        result: List[Tuple[str, str]] = []
        with self.__file.open() as file:
            lines: List[str] = file.readlines()
            for line in lines:
                if line[0] != "#":  # otherwise, line is comment
                    words: List[str] = line.split(" ")
                    if (
                        len(words) >= 3 and words[1] == "="
                    ):  # the general expression is met
                        key: str = words[0]
                        value_semicolon: str = words[2]
                        if len(value_semicolon) >= 2 and value_semicolon.__contains__(
                            ";"
                        ):  # pair is terminated by ';'
                            value: str = value_semicolon.split(";")[
                                0
                            ]  # only str before ';' is of interest
                            result.append((key, value))

        return result

    def __write_changes_to_file(self, changes: List[Tuple[str, str, str, str]]):
        """
        Takes a list of format (old_key, new_key, old_value, new_value) and replaces the old pairs in the file of the
        self with the corresponding new pairs. In this process the contents of the whole file are loaded into the
        working memory.
        An error is thrown if one of the old pairs isn't found in the file.
        """
        if changes:  # there has to be at least one change
            file: TextIO = open(self.get_file())
            content: str = file.read()
            file.close()
            for old_key, new_key, old_value, new_value in changes:
                old_line: str = old_key + " = " + old_value + ";"
                if old_line not in content:
                    raise InternalException(
                        "Internal Error: Pair: "
                        + str((old_key, old_value))
                        + "doesn't occur in file: "
                        + self.get_file_name()
                    )
                new_line: str = new_key + " = " + new_value + ";"
                content = content.replace(old_line, new_line)
            file = open(self.get_file(), "w")
            file.write(content)
            file.close()
