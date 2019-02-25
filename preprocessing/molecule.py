"""Defines a Molecule class.
"""

class Molecule:
    """Data model for a molecule. Stores the Pubchem ID, common name,
    and a tuple of flavor profiles.
    """
    def __init__(self, pubchem_id: int, name: str, flavor_profiles: tuple):
        assert pubchem_id is not None, "pubchem_id must be supplied"
        assert name is not None, "name must be supplied"
        assert flavor_profiles is not None, "flavor_profiles must be supplied"

        self.pubchem_id = pubchem_id
        self.name = name
        self.flavor_profiles = flavor_profiles

    def get_flavor_profiles(self):
        """Returns the molecule's flavor profiles.
        """
        return self.flavor_profiles

    def get_name(self):
        return self.name

    def get_pubchem_id(self):
        return self.pubchem_id
