from typing import List, Tuple
import pytest
import sys
sys.path.append("../../")
from preprocessing.main import create_mappings
from models.ingredient import Ingredient, IngredientType
from models.graph import Graph

class TestGraph:
    sample_mappings: List[Tuple[Ingredient, Ingredient, int]] = create_mappings("./data")

    def test_initialises_graph(self):
        G = Graph(self.sample_mappings)
        assert G is not None

    def test_can_get_node_by_name(self):
        G = Graph(self.sample_mappings)
        spinach = G.get_node_by_name("spinach")
        assert spinach is not None
        assert spinach.get_name() == "spinach"

    def test_can_get_neighbors_of_node(self):
        G = Graph(self.sample_mappings)
        spinach = G.get_node_by_name("spinach")
        spinach_nbrs = G.get_neighbors_of(spinach)
        assert spinach_nbrs is not None
        spinach_nbrs_filtered = G.get_neighbors_of(spinach, IngredientType.BASE)
        assert spinach_nbrs_filtered is not None

    def test_can_get_closest_neighbors_of_node(self):
        G = Graph(self.sample_mappings)
        spinach = G.get_node_by_name("spinach")
        spinach_nbrs = G.get_neighbors_of(spinach)
        # Sort neighbors of spinach from weakest to strongest so
        # we can then compare the first element of the array with
        # the array returned from the closest_neighbors() call.
        spinach_nbrs_weakest = sorted(spinach_nbrs, key=lambda node: node[1]["weight"])
        spinach_nbrs_closest = G.closest_neighbors(spinach, 1)
        assert spinach_nbrs_weakest[0] != spinach_nbrs_closest[0]
