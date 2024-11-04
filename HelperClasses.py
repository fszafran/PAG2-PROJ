from typing import List, Tuple, Set, Dict
from enum import Enum

class Edge:
    def __init__(self, id: int, id_from: str, id_to: str, length: float, road_category: float, number_of_attractions: int):
        self.id = id
        self.id_from = id_from
        self.id_to = id_to
        self.length = length
        self.road_category = road_category
        self.number_of_attractions = number_of_attractions

    def get_end(self) -> str:
        return self.id_to
    
    def cost_length(self) -> float:
        return self.length
    
    def cost_time(self) -> float:
        return self.length / self.road_category
    
    def cost_attractions(self) -> int:
        return self.number_of_attractions

    def __repr__(self) -> str:
        return f"Edge {self.id} from {self.id_from} to {self.id_to}"

    def __hash__(self) -> int:
        return hash((self.id_from, self.id_to, self.length))

    def __eq__(self, other: 'Edge') -> bool:
        return (self.id_from, self.id_to, self.length) == (other.id_from, other.id_to, other.length)

class Node:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.id = self.generate_id()
        self.edges = set()

    def generate_id(self) -> str:
        return f"{self.x}_{self.y}"

    def add_edge(self, edge: Edge):
        self.edges.add(edge)

    def get_neighbours(self) -> List[Tuple[Edge, str]]:
        return [(edge, edge.get_end()) for edge in self.edges]
    
    def __repr__(self) -> str:
        return f"Node {self.id}"
    
class Graph:
    def __init__(self):
        self.graph: Dict[str, Node] = {}

    def add_node(self, node: Node):
        if node.id not in self.graph:
            self.graph[node.id] = node

    def add_edge(self, edge: Edge):
        if edge.id_from in self.graph:
            self.graph[edge.id_from].add_edge(edge)

        if edge.id_to in self.graph:
            reversed_edge = Edge(edge.id, edge.id_to, edge.id_from, edge.length, edge.road_category, edge.number_of_attractions)
            self.graph[edge.id_to].add_edge(reversed_edge)

class Category(Enum):
    AUTOSTRADA = 140
    EKSPRESOWA = 120
    GLOWNA_RUCHU_PRZYSPIESZONEGO = 100
    GLOWNA = 90
    ZBIORCZA = 70
    LOKALNA = 50
    DOJAZDOWA = 30
    INNA = 20
    BRAK_KATEGORII = 5

class CategoryFactory:
    @staticmethod
    def get_category(category: str) -> Category:
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
