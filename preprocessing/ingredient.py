"""Defines the Ingredient class to store processed information on an ingredient.
"""
import json
from typing import List, Tuple, Dict
import math
from molecule import Molecule

FlavorProfiles = List[Tuple[str, int]]

class Ingredient:
    """An ingredient extracted from the FlavorDB database.
    """
    def __init__(self, name: str, category: str, flavor_db_entity_id: int,
                 molecules: List[Molecule]):
        self.name = name.lower()
        self.category = category.lower()
        self.id = flavor_db_entity_id
        self.molecules = molecules
        self.flavor_profiles = self._extract_flavor_profiles_from_molecules()

    def __str__(self):
        return f"{self.name} - {self.category} : {self.id}"

    def _extract_flavor_profiles_from_molecules(self) -> FlavorProfiles:
        """ Returns a sorted list of flavor profiles and associated counts
        extracted from the molecules in this ingredient
        """
        profiles: Dict[str, int] = {}
        for m in self.molecules:
            for fp in m.get_flavor_profiles():
                if fp not in profiles:
                    profiles[fp] = 1
                else:
                    profiles[fp] += 1

        sorted_profiles: FlavorProfiles = []
        for k, v in profiles.items():
            sorted_profiles.append((k, v))

        return sorted(sorted_profiles, key=lambda tup: tup[1], reverse=True)

    def get_top_flavors(self, pct: int = 25) -> FlavorProfiles:
        """ Returns the top pct of flavors represented by the molecules present
        in this ingredient. If no pct is supplied, defaults to 25%. The ceiling
        is used when the cutoff index is computed.
        """
        profiles: FlavorProfiles = self._extract_flavor_profiles_from_molecules()
        cutoff_idx: int = math.ceil(len(profiles) * (pct/100))
        return self.flavor_profiles[:cutoff_idx]

    def get_top_flavor(self) -> str:
        """Returns the top flavor from the flavor_profiles array.
        """
        return self.flavor_profiles[0]

    def json(self):
        """Returns a stringified JSON representation of the ingredient.
        """
        return json.dumps(self.__dict__)

