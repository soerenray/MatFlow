from __future__ import annotations
from typing import List, Tuple
from flask import request
from Implementierung.FrontendAPI import keys
import json


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

    def encode_config(self) -> dict:
        """
        extracts all reduced_config attributes and dumps them into json object

        Returns:
            String: json-dumped object containing encoded reduced config file (essentially key value pairs)
        """
        out_dict = dict({keys.config_file_name: self.get_file_name()})
        key_value_pairs: List[Tuple[str, str]] = self.get_key_value_pairs()
        out_dict.update({keys.key_value_pairs_name: key_value_pairs})
        return out_dict

    @classmethod
    def extract_config(cls, request_details: request) -> ReducedConfigFile:
        """
        extracts json details and builds a new ReducedConfigFile based off of these json details

        Args:
            request_details(request): contains encoded reduced config file

        Returns:
            ReducedConfigFile: the extracted reduced config file
        """
        decoded_json: dict = json.loads(request_details.get_json())
        name: str = decoded_json[keys.config_file_name]
        key_value_pairs: List[Tuple[str, str]] = decoded_json[keys.key_value_pairs_name]
        reduced_config: ReducedConfigFile = ReducedConfigFile(name, key_value_pairs)
        return reduced_config

    @classmethod
    def extract_multiple_configs(cls, request_details: request) -> List[ReducedConfigFile]:
        """
        extracts json details and builds a new ReducedConfigFile array based off of these json details

        Args:
            request_details(request): contains encoded reduced config files

        Returns:
            ReducedConfigFile[]: the extracted reduced config files
        """
        decoded_json: dict = json.loads(request_details.get_json())
        lists_of_json_configs: List[dict] = decoded_json[keys.config_files]
        configs: List[ReducedConfigFile] = []
        for json_config in lists_of_json_configs:
            config = ReducedConfigFile(json_config[keys.config_file_name], json_config[keys.key_value_pairs_name])
            configs.append(config)
        return configs
