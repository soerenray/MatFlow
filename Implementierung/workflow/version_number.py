class VersionNumber():
    """
    This class represents string expressions that are valid version numbers
    """
    def __init__(self, number: str):
        """Private Constructor of class VersionNumber. Call "fromString()" instead.

        Assumes the given String has correct syntax.

        Args:
            number (str): The version number
        """
        self.__number = number

    @ClassMethod
    def fromString(number: str)-> VersionNumber:
        """Translates correct string expressions into VersionNumber objects

        Only works if the expression is correct. Otherwise throws error.

        Args:
            number (str): The version number

        Returns:
            VerisonNumber: The created object
        """
        pass

    #getter

    def get_number(self)-> str:
        """Gets the version number stored in this object.

        Returns:
            str: Version number
        """
        return self.__number

    #setter

    def set_number(self, number: str):
        """Sets the number attribute of the object.

        Args:
            number (str): The new number that has to be a correct version number
        """
        self.__number = number