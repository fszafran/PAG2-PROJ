import unittest
from testGraphGenerator import *
from algorithm import algorithm

class testAlgorithm(unittest.TestCase):

    def test_algorithm_length(self):
        """
        Powinien zwrocic rzeczywista NAJKROTSZA droge od A do F: A -> B -> D -> F
        """
        graph = ABCDEF_1()
        self.assertEqual(
            [node.id for node in algorithm(graph, [1, 1], [4, 3], 1)],
            [Node(1, 1).id, Node(2, 3).id, Node(3, 3).id, Node(4, 3).id]
        )

    def test_algorithm_time(self):
        """
        Sztucznie obciazamy droge AB (nadajac predkosc 100), a dluzszej drodze AC (predkosc 140), 
        powinien zwrocic droge dluzsza, ale szybsza: A -> C -> E -> F
        """
        graph = ABCDEF_2()
        self.assertEqual(
            [node.id for node in algorithm(graph, [1, 1], [4, 3], 0)],
            ['1_1', '4_1', '4_2', '4_3']
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
            [node.id for node in algorithm(graph, [7, 1], [7, 4], 2)],
            ['7_1', '8_1', '10_1', '7_4']
        )

if __name__ == '__main__':
    unittest.main()