import pytest
from typing import List, Dict
from models.ingredient import IngredientType, Ingredient
from .main import construct_ingredient, calculate_similarity

test_json: Dict = {
    "category_readable": "Bakery",
    "entity_id": 484,
    "entity_alias_readable": "Pasta",
    "molecules": [
        {
            "fooddb_flavor_profile": "new mown hay@bitter@green@sweet@tonka",
            "pubchem_id": 323,
            "common_name": "coumarin"
        },
        {
            "fooddb_flavor_profile": "bitter",
            "pubchem_id": 107971,
            "common_name": "Daidzin"
        }
    ]
}

test_json_2: Dict = {
    "category_readable": "Bakery",
    "entity_id": 485,
    "entity_alias_readable": "Not Pasta",
    "molecules": [
        {
            "fooddb_flavor_profile": "new mown hay@bitter@green@sweet@tonka",
            "pubchem_id": 325,
            "common_name": "coumarin"
        },
        {
            "fooddb_flavor_profile": "bitter",
            "pubchem_id": 107971,
            "common_name": "Daidzin"
        }
    ]
}


class TestMain:
    def test_construct_ingredient(self):
        ing: Ingredient = construct_ingredient(test_json, "base")
        
        assert ing.get_name() == "pasta"
        assert ing.get_molecule_ids() == [323, 107971]
        assert ing.get_category() == "bakery"
        assert ing.get_type() == IngredientType.BASE

    def test_similarity(self):
        ing_1: Ingredient = construct_ingredient(test_json, "base")
        ing_2: Ingredient = construct_ingredient(test_json_2, "base")

        assert calculate_similarity(ing_1, ing_2) == 1
