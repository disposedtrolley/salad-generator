""" Preprocesses the JSON files downloaded from FlavorDB into a set of
ingredients and their molecules.
"""
import os
import sys
sys.path.append(".")
from typing import Dict, List
import json
from models.ingredient import Ingredient, FlavorProfiles
from models.molecule import Molecule

def read_data(root_path: str) -> List[Dict]:
    """ Reads all JSON files within a specified root directory, where
    subfolders of the directory are used as the "type" property of the
    ingredient.
    """
    ingredients: List[Dict] = []

    for root, _, files in os.walk(root_path):
        for name in files:
            file_path: str = os.path.join(root, name)
            ingredients.append(read_json(file_path))

    return ingredients

def read_json(path: str) -> Dict:
    """ Reads the file at the supplied path into a dictionary.
    """
    input_file = open(path, "r")
    contents: str = input_file.read()
    return json.loads(contents)

def __main__():
    i = read_data("./data")
    print(i[0])

if __name__ == "__main__":
    __main__()
