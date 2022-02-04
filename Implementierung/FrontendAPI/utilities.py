import os
from base64 import b64encode, b64decode
from pathlib import Path
from Implementierung.FrontendAPI import keys


parent_path: Path = Path(os.path.dirname(__file__))
temp_in_path: str = os.path.join(parent_path, keys.temp_in_name)


def create_dir(path: str) -> str:
    """
    creates a directory with unique identifier to prevent overwriting
    """
    created_dir: bool = False
    counter: int = 0
    while not created_dir:
        try_path: str = path + keys.underscore + str(counter)
        if not os.path.isdir(try_path):
            os.makedirs(try_path)
            return try_path
        counter += 1


def encode_file(file_path: Path, key: str) -> dict:
    """
    encodes a file in base64 encoding

    Args:
        file_path(Path): path to file
        key(String): key for json object

    Returns:
        dictionary with encoded file
    """
    out_dict: dict = dict()
    with open(file_path, "rb") as file:
        out_dict.update({key: b64encode(file.read())})
    os.remove(file_path)
    return out_dict


def decode_file(encoded_file: str):
    """
    decodes a file in base64 encoding

    Args:
        encoded_file(str): encoded file

    Returns:
        decoded file
    """
    return b64decode(encoded_file)
