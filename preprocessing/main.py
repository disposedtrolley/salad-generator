""" Preprocesses the JSON files downloaded from FlavorDB into a set of
ingredients and their molecules.
"""
import os
import sys
sys.path.append(".")
from typing import Dict, List, Tuple
import json
from models.ingredient import Ingredient, FlavorProfiles, IngredientType
from models.molecule import Molecule

def read_data(root_path: str) -> List[Ingredient]:
    """ Reads all JSON files within a specified root directory, where
    subfolders of the directory are used as the "type" property of the
    ingredient. Returns a list of Ingredient objects.
    """
    ingredients: List[Ingredient] = []

    for root, _, files in os.walk(root_path):
        for name in files:
            file_path: str = os.path.join(root, name)
            parent_folder_name: str = file_path.split("/")[2]
            ingredient: Ingredient = construct_ingredient(read_json(file_path),
                                                          parent_folder_name)
            ingredients.append(ingredient)

    return ingredients

def read_json(path: str) -> Dict:
    """ Reads the file at the supplied path into a dictionary.
    """
    input_file = open(path, "r")
    contents: str = input_file.read()
    return json.loads(contents)

def construct_ingredient(json: Dict, type: str) -> Ingredient:
    """ Returns an Ingredient object from a given JSON file
    """
    ingredient_type = IngredientType(type)

    molecules: List[Molecule] = [Molecule(m["pubchem_id"], m["common_name"],
                                          tuple(m["fooddb_flavor_profile"].split("@")))
                                          for m in json["molecules"]]
    return Ingredient(json["entity_alias_readable"], json["category_readable"],
                      json["entity_id"], molecules, ingredient_type)

def calculate_similarity(ing_a: Ingredient, ing_b: Ingredient) -> float:
    """ Returns the number of shared molecules between the supplied
    ingredients.
    """
    ing_a_molecules = ing_a.get_molecule_ids()
    ing_b_molecules = ing_b.get_molecule_ids()

    similar: List = list(set(ing_a_molecules).intersection(ing_b_molecules))

    return len(similar)

def __main__():
    all_ings: List[Ingredient] = read_data("./data")

    """
    Similarity mapping: 
    (pasta, chicken, 5)
    (pasta, apple, 1)
    (chicken, mushroom, 4)
    """
    
    mappings: List[Tuple[Ingredient, Ingredient, int]] = []

    for i in range(len(all_ings) -1):
        for x in range(len(all_ings) -1):
            if i != x:
                ing_a: Ingredient = all_ings[i]
                ing_b: Ingredient = all_ings[x]
                similarity: int = calculate_similarity(ing_a, ing_b)
                mappings.append((ing_a, ing_b, similarity))
    
    mappings.sort(key=lambda tup: tup[2])

    for m in mappings:
        print(m)

if __name__ == "__main__":
    __main__()
