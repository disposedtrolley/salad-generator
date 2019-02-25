from typing import Dict, List
import math

# FlavorProfile is an ordered array of flavors and the count of their
# occurrences, ordered from the highest to lowest occurring flavor.
# [{"bitter": 5, "sweet: 1"}]
FlavorProfiles = List[Dict[str, any]]

"""
An ingredient extracted from the FlavorDB database.
"""
class Ingredient:

    def __init__(self, name: str, category: str, flavor_db_entity_id: int,
                 flavor_profiles: FlavorProfiles):
        self.name = name
        self.category = category
        self.id = flavor_db_entity_id
        self.flavor_profiles = flavor_profiles

    def __str__(self):
        return f"{self.name} - {self.category} : {self.id}"

    """
    Returns the top pct of flavors from the flavor_profile. If no pct is
    supplied, defaults to 25%. The ceiling is used when the cutoff index
    is computed.
    """
    def get_top_flavors(self, pct: int = 25) -> FlavorProfiles:
        cutoff_idx = math.ceil(len(self.flavor_profiles) * (pct/100))
        return self.flavor_profiles[:cutoff_idx]
