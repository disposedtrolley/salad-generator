import sys
sys.path.append("..")
from typing import Dict, List, Tuple
from models.ingredient import IngredientType
from models.graph import Graph

class Traverser:
    """
    Provides methods to traverse an ingredient graph generated
    during preprocessing. A traversal through the graph means
    starting at some ingredient and recursively presenting the
    next best candidates according to an aggregate strength
    calculation.
    """

    # Define the limits around a valid salad composition.
    # Traversal can optionally conclude after the minimums
    # are reached, and must terminate once the maximums are
    # reached.
    salad_composition_limits = {
        IngredientType.BASE: (1, 2),
        IngredientType.TOPPING: (3, 6),
        IngredientType.PROTEIN: (1, 2),
        IngredientType.DRESSING: (1, 1)
    }

    def __init__(self, graph: Graph, limits):
        self.graph = graph
        self.ingredients = graph.get_nodes()
        self.salad_composition = []

        # Override standard limits if supplied.
        if limits:
            self.salad_composition_limits = limits

        self.start_traversal()

    def start_traversal(self):
        """
        Begins the ingredient graph traversal process.
        """
        assert self.graph is not None
        assert self.ingredients is not None
        assert len(self.ingredients) >= 1
        self._print_ingredient_choices(self._get_remaining_candidates())

    def get_limits(self):
        return self.salad_composition_limits

    def _get_remaining_candidates(self):
        """
        Returns a list of strongest remaining ingredient candidates
        based on:

        1) The state of the current salad composition as compared
           to the limits.
        2) The aggregate strength of the shared molecules of
           previously selected ingredients to unselected candidates.
        """
        return self.ingredients

    def _filter_composition_on_ingredient_type(self, ingredient_type):
        filtered_list = list(filter(lambda ig: ig.type == ingredient_type, self.salad_composition))
        return filtered_list

    def _can_add_more(self, ingredient_type):
        """
        Returns a boolean indicating if more of the specified ingredient_type
        can be added to the salad composition without reaching its limits.
        """
        allowable_range = self.salad_composition_limits[ingredient_type]
        filtered_list = \
            self._filter_composition_on_ingredient_type(ingredient_type)
        return len(filtered_list) < allowable_range[1]

    def _needs_more(self, ingredient_type):
        """
        Returns a boolean indicating if more of the specified ingredient_type
        must be added to the salad composition before the minimum required
        number is reached.
        """
        allowable_range = self.salad_composition_limits[ingredient_type]
        filtered_list = \
            self._filter_composition_on_ingredient_type(ingredient_type)
        return len(filtered_list) < allowable_range[0]

    def _print_ingredient_choices(self, remaining_choices):
        """
        Displays a list of ingredient choices for the user
        to select. The index of the ingredient is the choice
        key value.
        """
        for (idx, ingredient) in enumerate(remaining_choices):
            print(f"{idx}. {ingredient.name}")
