from typing import List, Tuple
import networkx as nx
import os
import sys
sys.path.append("../..")
from preprocessing.main import create_mappings
from models.ingredient import Ingredient, IngredientType

"""
Wraps the Networkx graph class to provide additional functionality relevant to salad generation,
including convenience methods for returning the closest neighbours of a given ingredient.
"""
class Graph:
    """
    Instantiates a Graph object by creating a Networkx graph from a given list of
    ingredient mappings.
    """
    def __init__(self, mappings: List[Tuple[Ingredient, Ingredient, int]]):
        self.G = nx.Graph()
        for item in mappings:
            self.G.add_edge(item[0], item[1], weight=item[2])
        print(self.G)

    """
    Returns the node of the graph that matches the supplied ingredient name.
    """
    def get_node_by_name(self, name: str):
        for n in self.G:
            if n.get_name() == name:
                return n
        return None

    def get_nodes(self):
        return list(self.G.nodes)

    """
    Returns all neighbours of a given ingredient. Optionally filters the neighbors list
    to include only ingredients of a given type.
    """
    def get_neighbors_of(self, node, ingredient_type: IngredientType = None):
        for n, neighbors in self.G.adjacency():
            if node == n:
                if ingredient_type is None:
                    return neighbors.items()
                else:
                    return [node for node in neighbors.items()
                            if node[0].get_type() == ingredient_type]

    """
    Returns the closest neighbours of a given ingredient, the number of ingredients is specified
    by the count. Optionally filters the neighbors list to include only ingredients of a given type.
    """
    def closest_neighbors(self, node, count: int, ingredient_type: IngredientType = None):
        neighbors = self.get_neighbors_of(node, ingredient_type)
        sorted_neighbors = sorted(neighbors, key=lambda node: node[1]['weight'], reverse=True)
        return sorted_neighbors[:count]

    def get_weight_between(self, node_a: str, node_b: str):
        """
        Returns the weight between two given nodes from their names.
        """
        node_a_in_graph = self.get_node_by_name(node_a)
        node_b_in_graph = self.get_node_by_name(node_b)

        return self.G.get_edge_data(node_a_in_graph, node_b_in_graph)['weight']
