import pytest
from .molecule import Molecule

class TestMolecule:
    def test_checks_init_params(self):
        with pytest.raises(AssertionError) as e:
            m = Molecule(None, None, None)
        assert "pubchem_id must be supplied" in str(e.value)

    def test_gets_flavor_profiles(self):
        flavor_profiles: tuple = ("salty", "sweet")
        m = Molecule(1, "test", flavor_profiles)
        assert m.get_flavor_profiles() == flavor_profiles

    def test_gets_name(self):
        name: str = "test"
        m = Molecule(1, name, ())
        assert m.get_name() == name

    def test_gets_pubchem_id(self):
        id: int = 1
        m = Molecule(id, "test", ())
        assert m.get_pubchem_id() == id
