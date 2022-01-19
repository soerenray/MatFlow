class ParameterChange:
    """
    This class represents the change of a key-value pair.
    It contains the old as well as the new version of both the key and the value.
    Furthermore, it holds the name of the file the change was made in.
    """
    def __init__(self, old_key: str, new_key: str, old_value: str, new_value: str, config_file_name: str):
        """Constructor of class ParameterChange.

        Args:
            old_key (str): The key of the pair before the change
            new_key (str): The key of the pair after the change
            old_value (str): The value of the pair before the change
            new_value (str): The value of the pair after the change
            config_file_name (str): The name of the file in which the change was made
        """
        self.__old_key = old_key
        self.__new_key = new_key
        self.__old_value = old_value
        self.__new_value = new_value
        self.__config_file_name = config_file_name

    # getter

    def get_old_key(self) -> str:
        """Gets the old key of the key-value-pair.

        Returns:
            str: old key of the key-value-pair
        """
        return self.__old_key

    def get_new_key(self) -> str:
        """Gets the new key of the key-value-pair.

        Returns:
            str: new key of the key-value-pair
        """
        return self.__new_key

    def get_old_value(self) -> str:
        """Gets the old value of the key-value-pair.

        Returns:
            str: old value of the key-value-pair
        """
        return self.__old_value

    def get_new_value(self) -> str:
        """Gets the new value of the key-value-pair.

        Returns:
            str: new value of the key-value-pair
        """
        return self.__new_value

    def get_config_file_name(self) -> str:
        """Gets the name of the config file the change was made in.

        Returns:
            str: name of the config file
        """
        return self.__config_file_name

    # setter

    def set_old_key(self, old_key: str):
        """Sets the old_key attribute of the object.

        Args:
            old_key (str): Updated old key of the key-value-pair
        """
        self.__old_key = old_key

    def set_new_key(self, new_key: str):
        """Sets the new_key attribute of the object.

        Args:
            new_key (str): Updated new key of the key-value-pair
        """
        self.__new_key = new_key

    def set_old_value(self, old_value: str):
        """Sets the old_value attribute of the object.

        Args:
            old_value (str): Updated old value of the key-value-pair
        """
        self.__old_value = old_value

    def set_new_value(self, new_value: str):
        """Sets the new_value attribute of the object.

        Args:
            new_value (str): Updated new value of the key-value-pair
        """
        self.__new_value = new_value

    def set_config_file_name(self, config_file_name: str):
        """Sets the name of the config file the change was made in

        Args:
            config_file_name (str): The name of the config file
        """
        self.__config_file_name = config_file_name
