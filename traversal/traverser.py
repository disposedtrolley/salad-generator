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

    def __init__(self, graph: Graph, limits=None):
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

        while True:
            self._perform_traversal_iteration()

    def _perform_traversal_iteration(self):
        """
        Performs one interation of traversal through the ingredient
        graph by executing the following:

        1) Refreshing the ingredients instance property to remove used
           ingredients.
        2) Calculating the next best candidates.
        3) Presenting the choices to the user.
        4) Capturing the next choice taken by the user.
        """
        self._pop_used_ingredients()
        next_candidates = self._get_next_candidates()
        self._print_ingredient_choices(next_candidates)

        # @TODO clearly the index selected by the user belongs to the
        # temporary candidates list and not our ingredients instance property
        # duh.
        selected_ing = self.ingredients[self._get_user_selection()]

        self.add_ingredient_to_composition(selected_ing)

    def _get_user_selection(self):
        selection = -1
        while selection < 0 or selection > len(self.ingredients):
            selection = int(input("Choose an ingredient: "))
        return selection

    def get_limits(self):
        return self.salad_composition_limits

    def _get_next_candidates(self):
        """
        Returns a list of strongest remaining ingredient candidates
        based on:

        1) The state of the current salad composition as compared
           to the limits.
        2) The aggregate strength of the shared molecules of
           previously selected ingredients to unselected candidates.
        """
        candidates = []  # List of tuples of (Ingredient, Aggregate Strength)

        for candidate in self.ingredients:
            # Calculate the aggregate strength between the candidate ingredient
            # and all ingredients in the salad composition.
            aggregate_strength = 0

            for ing in self.salad_composition:
                aggregate_strength += self.graph.get_weight_between(ing.get_name(),
                                                                candidate.get_name())
            candidates.append((candidate, aggregate_strength))

        return sorted(candidates, key=lambda c: c[1], reverse=True)

    def _pop_used_ingredients(self):
        """
        Removes items from the ingredients instance property which have
        been incorporated into the salad composition.
        """
        self.ingredients = [i for i in self.ingredients if i not in
                            self.salad_composition]

    def get_composition(self):
        return self.salad_composition

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

    def add_ingredient_to_composition(self, ingredient):
        self.salad_composition.append(ingredient)

    def _print_ingredient_choices(self, candidates):
        """
        Displays a list of ingredient choices for the user
        to select. The index of the ingredient is the choice
        key value.
        """
        for (idx, candidate) in enumerate(candidates):
            print(f"{idx:<10} {candidate[0].name:<20} {candidate[1]:<10}")
