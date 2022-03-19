import os.path
import shutil
from pathlib import Path
from os import listdir
from matflow.workflow.template import Template
from matflow.exceptionpackage.MatFlowException import EmptyConfigFolderException


class WorkflowInstance(Template):
    """
    This class represents a workflow instance.
    It contains the identifying name of the instance, a dag-definition-file as well as a folder with input files.
    """

    __config_folder: Path

    def __init__(self, name: str, dag_definition_file: Path, config_folder: Path):
        """Constructor of class WorkflowInstance.

        Only works if the referenced dag definition file is valid.

        Args:
            name (str): The name of the new workflow instance
            dag_definition_file (Path): Path of the file which defines the behavior of the workflow instance
            config_folder (Path): Path to a directory of input files needed for executing the workflow

        """
        super().__init__(name, dag_definition_file)
        if not listdir(config_folder):  # the config folder is empty
            raise EmptyConfigFolderException("")  # TODO
        self.__config_folder = config_folder
        self.__name = name
        self.__dag_definition_file = dag_definition_file

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

    # other methods

    def activate_instance(self, dags_folder: Path):
        """Performs changes to the dag_definition_file such that the dag_id inside the file matches the name of the
        WorkflowInstance object. After that the file is copied to the given path

        Args:
            dags_folder (Path): The path where the changed dag definition file belongs

        """
        shutil.copyfile(self.__dag_definition_file, os.path.join(dags_folder, (self.__name + ".py")))

        # p = Path(__file__)
        # root -> matflow -> workflow -> workflow_instance.py
        # parent_path = Path(p.parent.parent.parent.absolute())
        # root -> dags
        # dag_path = os.path.join(parent_path, "dags", (self.__name + ".py"))
        # copy from dag_folder to dag path
        # shutil.copyfile(dags_folder.absolute(), Path(dag_path))"""
