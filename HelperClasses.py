class Edge:
    def __init__(self, id, id_from, id_to, length, road_category, number_of_attractions):
        self.id = id
        self.id_from = id_from
        self.id_to = id_to
        self.length = length
        self.road_category = road_category
        self.number_of_attractions = number_of_attractions

    def __repr__(self):
        return f"Edge {self.id} from {self.id_from} to {self.id_to}"

    def __hash__(self):
        return hash((self.id_from, self.id_to, self.length))

    def __eq__(self, other):
        return (self.id_from, self.id_to, self.length) == (other.id_from, other.id_to, other.length)

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = self.generate_id()
        self.edges = set()

    def generate_id(self):
        return f"{self.x}_{self.y}"

    def add_edge(self, edge):
        self.edges.add(edge)

    def __repr__(self):
        return f"Node {self.id}"
    
class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        if node.id not in self.graph:
            self.graph[node.id] = node

    def add_edge(self, edge):
        if edge.id_from in self.graph:
            self.graph[edge.id_from].add_edge(edge)

        if edge.id_to in self.graph:
            reversed_edge = Edge(edge.id, edge.id_to, edge.id_from, edge.length, edge.road_category, edge.number_of_attractions)
            self.graph[edge.id_to].add_edge(reversed_edge)

    def __repr__(self):
        for key, value in self.graph.items():
            print(f"{key}: {value.edges}")

    def __str__(self):
        return self.__repr__()

from enum import Enum
class Category(Enum):
    AUTOSTRADA = 140
    EKSPRESOWA = 120
    GLOWNA_RUCHU_PRZYSPIESZONEGO = 100
    GLOWNA = 90
    ZBIORCZA = 70
    LOKALNA = 50
    DOJAZDOWA = 30
    INNA = 20
    BRAK_KATEGORII = 1

class CategoryFactory:
    @staticmethod
    def get_category(category):
        if category == "A":
            return Category.AUTOSTRADA
        elif category == "S":
            return Category.EKSPRESOWA
        elif category == "GP":
            return Category.GLOWNA_RUCHU_PRZYSPIESZONEGO
        elif category == "G":
            return Category.GLOWNA
        elif category == "Z":
            return Category.ZBIORCZA
        elif category == "L":
            return Category.LOKALNA
        elif category == "D":
            return Category.DOJAZDOWA
        elif category == "I":
            return Category.INNA
        else:
            return Category.BRAK_KATEGORII
