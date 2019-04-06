import sys
sys.path.append("..")
import pytest
from preprocessing.main import create_mappings
from models.graph import Graph
from .traverser import Traverser

class TestTraverser:
    mappings = create_mappings("./data")
    G = Graph(mappings)

    def test_init(self):
        t = Traverser(self.G)
        assert t is not None
