import pytest
from typing import List
from ingredient import Ingredient, FlavorProfiles
from molecule import Molecule

sample_molecules: List[Molecule] = [
    Molecule(323, "coumarin", ("bitter", "green", "sweet")),
    Molecule(107971, "Daidzin", ("bitter",)),
    Molecule(7284, "2-Methy1butyra1dehyde", ("musty", "coffee", "cocoa",
                                             "nutty", "almond"))]

expected_flavor_profiles: FlavorProfiles = [
            ("bitter", 2),
            ("green", 1),
            ("sweet", 1),
            ("musty", 1),
            ("coffee", 1),
            ("cocoa", 1),
            ("nutty", 1),
            ("almond", 1)]

class TestIngredient:
    def test_sets_instance_vars(self):
        pasta = Ingredient("Pasta", "Bakery", 484, sample_molecules)
        assert pasta.name == "pasta"
        assert pasta.category == "bakery"
        assert pasta.id == 484
        assert pasta.molecules == sample_molecules

    def test_extract_flavor_profiles_from_molecules(self):
        pasta = Ingredient("Pasta", "Bakery", 484, sample_molecules)

        assert pasta._extract_flavor_profiles_from_molecules()  == expected_flavor_profiles

    def test_get_top_flavors(self):
        pasta = Ingredient("Pasta", "Bakery", 484, sample_molecules)

        assert pasta.get_top_flavors() == expected_flavor_profiles[:2]

    def test_get_top_flavor(self):
        pasta = Ingredient("Pasta", "Bakery", 484, sample_molecules)

        assert pasta.get_top_flavor() == expected_flavor_profiles[0]

    def test_json(self):
        pass
