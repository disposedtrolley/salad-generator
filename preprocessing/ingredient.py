from typing import Dict, List
import math

# FlavourProfile is an ordered array of flavours and the count of their
# occurrences, ordered from the highest to lowest occurring flavour.
# [{"bitter": 5, "sweet: 1"}]
FlavourProfiles = List[Dict[str, any]]

"""
An ingredient extracted from the FlavorDB database.
"""
class Ingredient:

    def __init__(self, name: str, category: str, flavor_db_entity_id: int,
                 flavour_profiles: FlavourProfiles):
        self.name = name
        self.category = category
        self.id = flavor_db_entity_id
        self.flavour_profiles = flavour_profiles

    def __str__(self):
        return f"{self.name} - {self.category} : {self.id}"

    """
    Returns the top pct of flavours from the flavour_profile. If no pct is
    supplied, defaults to 25%.
    """
    def get_top_flavors(self, pct: int = 25) -> FlavourProfiles:
        cutoff_idx = math.floor(len(self.flavour_profiles) * (25/100))
        return self.flavour_profiles[:cutoff_idx]
