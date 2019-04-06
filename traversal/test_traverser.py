import sys
sys.path.append("..")
import pytest
from preprocessing.main import create_mappings
from models.graph import Graph
from models.ingredient import IngredientType
from .traverser import Traverser

default_limits = {
    IngredientType.BASE: (1, 2),
    IngredientType.TOPPING: (3, 6),
    IngredientType.PROTEIN: (1, 2),
    IngredientType.DRESSING: (1, 1)
}

custom_limits = {
    IngredientType.BASE: (2, 4),
    IngredientType.TOPPING: (1, 2),
    IngredientType.PROTEIN: (2, 2),
    IngredientType.DRESSING: (1, 4)
}

class TestTraverser:
    mappings = create_mappings("./data")
    G = Graph(mappings)

    def test_init(self):
        t = Traverser(self.G)
        assert t is not None

    def test_default_and_custom_limits(self):
        t = Traverser(self.G)
        assert t.get_limits() == default_limits

        t = Traverser(self.G, custom_limits)
        assert t.get_limits() == custom_limits

    def test_limit_helpers(self):
        t = Traverser(self.G)

        # Check default limits are computed properly.
        assert t._can_add_more(IngredientType.BASE) is True
        assert t._needs_more(IngredientType.BASE) is True

        ing_base_pasta = self.G.get_node_by_name("pasta")
        ing_base_spinach = self.G.get_node_by_name("spinach")

        # Add one base to the composition. Default limits says we can have a
        # minimum of one base and a maximum of two, so _can_add_more() should
        # be True as we have not reached the maximum, but _needs_more() should
        # be False as we've reached the minimum.
        t.add_ingredient_to_composition(ing_base_pasta)
        assert t._can_add_more(IngredientType.BASE) is True
        assert t._needs_more(IngredientType.BASE) is False

        # Add another base to the composition. We now should have reached the
        # maximum allowed by the default limits.
        t.add_ingredient_to_composition(ing_base_spinach)
        assert t._can_add_more(IngredientType.BASE) is False
        assert t._needs_more(IngredientType.BASE) is False

    def test_composition_filtering(self):
        t = Traverser(self.G)
        assert t.get_composition() == []

        # Add some ingredients to the salad
        ing_tomato = self.G.get_node_by_name("tomato")
        ing_chicken = self.G.get_node_by_name("chicken")
        t.add_ingredient_to_composition(ing_tomato)
        assert t.get_composition() == [ing_tomato]
        t.add_ingredient_to_composition(ing_chicken)
        assert t.get_composition() == [ing_tomato, ing_chicken]

        # See if filtering works properly
        filtered_composition = \
            t._filter_composition_on_ingredient_type(IngredientType.TOPPING)
        assert filtered_composition == [ing_tomato]

        filtered_composition = \
            t._filter_composition_on_ingredient_type(IngredientType.PROTEIN)
        assert filtered_composition == [ing_chicken]

        # The instance variable shouldn't be mutated through filtering.
        assert t.get_composition() == [ing_tomato, ing_chicken]

