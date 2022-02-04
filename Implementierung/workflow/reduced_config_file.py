from __future__ import annotations

import os
from pathlib import Path
from typing import List, Tuple
from flask import request

from Implementierung.ExceptionPackage.MatFlowException import ConverterException
from Implementierung.FrontendAPI import keys, utilities
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
    def extract_config(cls, json_details: str) -> ReducedConfigFile:
        """
        extracts json details and builds a new ReducedConfigFile based off of these json details

        Args:
            json_details(str): contains encoded reduced config file

        Returns:
            ReducedConfigFile: the extracted reduced config file
        """
        decoded_json: dict = json.loads(json_details)
        if keys.config_file_name not in decoded_json:
            raise ConverterException("no file name")
        if keys.key_value_pairs_name not in decoded_json:
            raise ConverterException("no key value pairs")
        name: str = decoded_json[keys.config_file_name]
        key_value_pairs: List[Tuple[str, str]] = decoded_json[keys.key_value_pairs_name]
        reduced_config: ReducedConfigFile = ReducedConfigFile(name, key_value_pairs)
        return reduced_config

    @classmethod
    def extract_multiple_configs(cls, json_details: str) -> List[ReducedConfigFile]:
        """
        extracts json details and builds a new ReducedConfigFile array based off of these json details

        Args:
            json_details(str): contains encoded reduced config files

        Returns:
            ReducedConfigFile[]: the extracted reduced config files
        """
        decoded_json: dict = json.loads(json_details)
        if keys.config_files not in decoded_json:
            raise ConverterException("no files")
        lists_of_json_configs: List[dict] = decoded_json[keys.config_files]
        configs: List[ReducedConfigFile] = []
        # {configFiles: [{configFileName: "scooby", keyValuePairs:[("ha", "he")]}, ..]}
        for json_config in lists_of_json_configs:
            if keys.config_file_name not in json_config:
                raise ConverterException("no config file name")
            if keys.key_value_pairs_name not in json_config:
                raise ConverterException("no key value pairs")
            config = ReducedConfigFile(
                json_config[keys.config_file_name],
                json_config[keys.key_value_pairs_name],
            )
            configs.append(config)
        return configs

    @classmethod
    def extract_multiple_config_files(cls, json_details: str) -> Path:
        """
        extracts encoded config files and dumps them into a temporary directory

        Args:
            json_details(str): contains encoded config files

        Returns:
            Path to saved configs
        """
        decoded_json: dict = json.loads(json_details)
        if keys.config_files not in decoded_json:
            raise ConverterException("no files key")
        save_dir: str = utilities.create_dir(
            os.path.join(
                utilities.parent_path, utilities.temp_in_path, keys.config_save_path
            )
        )
        lists_of_encoded_configs: List[dict] = decoded_json[keys.config_files]
        # config files are encoded like this: {configFiles: [{configFileName: "bla", file: "encoded_file"}, {..}, ..]}
        for encoded_config in lists_of_encoded_configs:
            if keys.file_key not in encoded_config:
                raise ConverterException("no file key")
            if keys.config_file_name not in encoded_config:
                raise ConverterException("no file provided")
            config_file = utilities.decode_file(encoded_config[keys.file_key])
            config_name = encoded_config[keys.config_file_name]
            with open(os.path.join(save_dir, config_name), "wb") as file:
                file.write(config_file)
        return Path(save_dir)
