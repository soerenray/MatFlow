from pathlib import Path
from workflow.template import Template


class WorkflowInstance(Template):
    """
    This class represents a workflow instance.
    It contains the identifying name of the instance, a dag-definition-file as well as a folder with input files.
    """
    def __init__(self, name: str, dag_definition_file: Path, config_folder: Path):
        """Constructor of class WorkflowInstance.

        Only works if the referenced dag definition file is valid.

        Args:
            name (str): The name of the new template
            dag_definition_file (Path): Path of the file which defines the behavior of workflows
            instantiated from this template
            config_folder (Path): Path to a directory of input files needed for executing the workflow

        """
        super().__init__(name, dag_definition_file)
        self.__config_folder = config_folder

    # getter

    def get_config_folder(self) -> Path:
        """Gets the path of the config folder of the object.

        Returns:
            Path: Path of the config folder

        """
        return self.__config_folder

    # setter

    def set_config_folder(self, config_folder: Path):
        """Sets the path of the config folder of the object.

        Args:
            config_folder (Path): The Path of the new config folder

        """
        self.__config_folder = config_folder
