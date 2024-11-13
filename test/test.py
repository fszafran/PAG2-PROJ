import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from testGraphGenerator import *
from algorithm import algorithm
import numpy as np

def heuristic(from_node_id: str, to_node_id: str) -> float:
    x1, y1 = map(float, from_node_id.split("_"))
    x2, y2 = map(float, to_node_id.split("_"))
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

class testAlgorithm(unittest.TestCase):

    def test_algorithm_length(self):
        """
        Powinien zwrocic rzeczywista NAJKROTSZA droge od A do F: A -> B -> D -> F
        """
        graph = ABCDEF_1()
        self.assertEqual(
            [node.id for node in algorithm(graph, [1, 1], [4, 3], heuristic, 1)],
            [Node(1, 1).id, Node(2, 3).id, Node(3, 3).id, Node(4, 3).id]
        )

    def test_algorithm_time(self):
        """
        Sztucznie obciazamy droge AB (nadajac predkosc 100), a dluzszej drodze AC (predkosc 140), 
        powinien zwrocic droge dluzsza, ale szybsza: A -> C -> E -> F
        """
        graph = ABCDEF_2()
        self.assertEqual(
            [node.id for node in algorithm(graph, [1, 1], [4, 3], heuristic, 0)],
            [Node(1, 1).id, Node(4,1).id, Node(4,2).id, Node(4, 3).id]
        )
        
    def test_algorithm_attractions(self):
        """
        Krawedzie maja odpowiednio:
        GH - 0 atrakcji
        HJ - 0 atrakcji
        GI - sporo atrakcji
        IK - malo atrakcji
        JK - maksymalnie duzo atrakcji
        Najkrotsza trasa to G -> H -> J, ale powinien wybrac G -> I -> K -> J
        """
        graph = GHIJK_1()
        self.assertEqual(
            [node.id for node in algorithm(graph, [7, 1], [7, 4], heuristic, 2)],
            [Node(7, 1).id, Node(8, 1).id, Node(10, 1).id, Node(7, 4).id]
        )

if __name__ == '__main__':
    unittest.main()