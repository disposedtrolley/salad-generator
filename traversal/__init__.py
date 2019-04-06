import sys
sys.path.append("..")
from models.ingredient import Ingredient, IngredientType
from models.graph import Graph
from preprocessing.main import create_mappings
from traversal.traverser import Traverser

if __name__ == "__main__":
    mappings = create_mappings("../data")
    g = Graph(mappings)
    t = Traverser(g)
