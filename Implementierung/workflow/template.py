from __future__ import annotations
from flask import request
from pathlib import Path
from Implementierung.ExceptionPackage.MatFlowException import InvalidDagFileException
from Implementierung.FrontendAPI import keys, utilities
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import os
import json


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
        if not Template.__dag_definition_file_is_valid(dag_definition_file):
            raise InvalidDagFileException("")  # TODO
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

    # static methods

    @staticmethod
    def __dag_definition_file_is_valid(file_path: Path) -> bool:
        # TODO better implementation
        return True

    @classmethod
    def extract_template(cls, request_details: request) -> Template:
        """
        extracts json details and builds a new Template based off of these json details

        Args:
            request_details(String): contains encoded template

        Returns:
            Template: decoded template object
        """
        decoded_json = json.loads(request_details.get_json())
        name: str = decoded_json[keys.template_name]
        file_path: Path = cls.extract_dag_file(decoded_json)
        template: Template = Template(name, file_path)
        return template

    @classmethod
    def extract_dag_file(cls, decoded_json: dict) -> Path:
        """
        saves the dag definition file to the hard drive

        Args:
            decoded_json(dict): contains dag definition file and template name

        Returns:
            path to saved file
        """

        dag_file = utilities.decode_file(decoded_json[keys.file_key])
        filename: str = secure_filename(dag_file.filename)
        save_dir: str = utilities.create_dir(os.path.join(utilities.parent_path, keys.temp_in_path,
                                                          keys.dag_save_path))
        file_path: str = os.path.join(save_dir, filename)
        dag_file.save(file_path)
        return Path(file_path)

    def encode_template(self) -> dict:
        """
        encodes all template attributes and dumps them into json object

        Returns:
            List[str]: all the needed information to upload file
        """
        out_dict: dict = dict()
        name: str = self.get_name()
        out_dict.update({keys.template_name: name})
        # path to file
        file_path: Path = self.get_dag_definition_file()
        out_dict.update({keys.file_key: utilities.encode_file(file_path, keys.dag_definition_name)})
        return out_dict
