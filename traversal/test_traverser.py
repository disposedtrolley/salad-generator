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

