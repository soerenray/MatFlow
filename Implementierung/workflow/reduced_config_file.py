from typing import List, Tuple


class ReducedConfigFile:
    """
    This class holds all information to represent a config-file in the frontend.
    """
    __file_name: str
    __key_value_pairs: List[Tuple[str, str]]

    def __init__(self, file_name: str, key_value_pairs: List[Tuple[str, str]]):
        """Constructor of class ReducedConfigFile.

        Args:
            file_name (str): The name of the config-file through which the config-file can be identified among other
            config files of the workflow instance
            key_value_pairs (list[tuple[str,str]]): The contents of the file in key-value-pair representation
        """
        self.__file_name = file_name
        self.__key_value_pairs = key_value_pairs

    # getter

    def get_file_name(self) -> str:
        """Gets the name of the config file.

        Returns:
            str: Name of the file

        """
        return self.__file_name

    def get_key_value_pairs(self) -> List[Tuple[str, str]]:
        """Gets the contents of the file in key-value-pair representation.

        Returns:
            list[tuple[str,str]]: The list of key-value-pairs

        """
        return self.__key_value_pairs

    # setter

    def set_file_name(self, file_name: str):
        """Sets the file_name attribute of the object.

        Args:
            file_name (str): The new name of the file

        """
        self.__file_name = file_name

    def set_key_value_pairs(self, key_value_pairs: List[Tuple[str, str]]):
        """Sets new list of key-value-pairs.

        Args:
            key_value_pairs (List[Tuple[str, str]]): The list of key-value-pairs

        """
        self.__key_value_pairs = key_value_pairs
