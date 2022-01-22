from pathlib import Path


class Template:
    """
    This class represents a workflow template.
    It contains the identifying name of the template as well as a dag-definition-file.
    """
    __name: str
    __dag_definition_file: Path

    def __init__(self, name: str, dag_definition_file: Path):
        """Constructor of class Template.

        Only works if the referenced dag definition file is valid.

        Args:
            name (str): The name of the new template
            dag_definition_file (Path): Path of the file which defines the behavior of workflows
            instantiated from this template
        """
        self.__name = name
        self.__dag_definition_file = dag_definition_file

    # getter

    def get_name(self) -> str:
        """Gets the name attribute of the object.

        Returns:
            str: Name of the template
        """
        return self.__name

    def get_dag_definition_file(self) -> Path:
        """Gets the path of the dag definition file of the object.

        Returns:
            Path: Path of the dag definition file
        """
        return self.__dag_definition_file

    # setter

    def set_name(self, name: str):
        """Sets the name attribute of the object.

        Args:
            name (str): The new name of the template
        """
        self.__name = name

    def set_dag_definition_file(self, dag_definition_file: Path):
        """Sets the path of the dag definition file of the object.

        Args:
            dag_definition_file (Path): The Path of the new dag definition file
        """
        self.__dag_definition_file = dag_definition_file
