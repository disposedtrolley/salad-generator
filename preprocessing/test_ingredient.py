import pytest
import ingredient

sample_flavor_profiles: ingredient.FlavorProfiles = [
    {"name": "sweet",
     "occurrences": 10},
    {"name": "sour",
     "occurrences": 8},
    {"name": "fruity",
     "occurrences": 8},
    {"name": "bitter",
     "occurrences": 6},
    {"name": "pungent",
     "occurrences": 5},
    {"name": "herbal",
     "occurrences": 2},
    {"name": "watery",
     "occurrences": 2},
    {"name": "candy",
     "occurrences": 2},
    {"name": "fresh",
     "occurrences": 2},
    {"name": "floral",
     "occurrences": 1}]

class TestIngredient(object):
    def test_sets_instance_vars(self):
        apple = ingredient.Ingredient("Apple",
                                      "Fruit",
                                      123,
                                      sample_flavor_profiles)

        assert(apple.name == "Apple")
        assert(apple.category == "Fruit")
        assert(apple.id == 123)
        assert(apple.flavor_profiles == sample_flavor_profiles)

    def test_get_top_flavors(self):
        apple = ingredient.Ingredient("Apple",
                                      "Fruit",
                                      123,
                                      sample_flavor_profiles)

        assert(apple.get_top_flavors() == sample_flavor_profiles[:3])
        assert(apple.get_top_flavors(10) == sample_flavor_profiles[:1])
