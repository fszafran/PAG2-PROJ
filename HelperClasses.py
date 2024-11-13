from typing import List, Tuple, Set, Dict
from enum import Enum

class Edge:
    def __init__(self, id: int, id_from: str, id_to: str, length: float, road_category: int, number_of_attractions: int):
        self.id = id
        self.id_from = id_from
        self.id_to = id_to
        self.length = length
        self.road_category = road_category
        self.number_of_attractions = number_of_attractions

    def get_end(self) -> str:
        return self.id_to
   
    def get_appropriate_cost(self, route_type: int) -> float:
        if route_type == 0:
            return (self.length / self.road_category)
        elif route_type == 1:
            return self.length
        elif route_type == 2:
            return self.number_of_attractions
        else:
            raise ValueError("Niepoprawny typ trasy, poprawne wartości to: 0, 1, 2")
    
    def __repr__(self) -> str:
        return f"From {self.id_from} to {self.id_to}"

    def __hash__(self) -> int:
        return hash((self.id_from, self.id_to, self.length))

    def __eq__(self, other: 'Edge') -> bool:
        return (self.id_from, self.id_to, self.length) == (other.id_from, other.id_to, other.length)

    def to_json(self) -> Dict:
        return {
            "id": self.id,
            "id_from": self.id_from,
            "id_to": self.id_to,
            "length": self.length,
            "road_category": self.road_category,
            "number_of_attractions": self.number_of_attractions
        }

class Node:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.id = self.generate_id()
        self.edges = set()

    def generate_id(self) -> str:
        x = round(self.x)
        y = round(self.y)
        return f"{x}_{y}"

    def add_edge(self, edge: Edge):
        self.edges.add(edge)

    def get_neighbours(self) -> List[Tuple[Edge, str]]:
        return [(edge, edge.get_end()) for edge in self.edges]
    
    def __repr__(self) -> str:
        return f"{self.id}"
    
    def to_json(self) -> Dict:
        return {
            "x": self.x,
            "y": self.y,
            "edges": [edge.to_json() for edge in self.edges]
        }

class Graph:
    def __init__(self, json_file: str = None):
        self.graph: Dict[str, Node] = {}
        if json_file:
            self.from_json(json_file)

    def add_node(self, node: Node):
        if node.id not in self.graph:
            self.graph[node.id] = node

    def add_edge(self, edge: Edge):
        if edge.id_from in self.graph:
            self.graph[edge.id_from].add_edge(edge)

        if edge.id_to in self.graph:
            reversed_edge = Edge(edge.id, edge.id_to, edge.id_from, edge.length, edge.road_category, edge.number_of_attractions)
            self.graph[edge.id_to].add_edge(reversed_edge)

    def from_json(self, json_dict: Dict):
        for _, node in json_dict.items():
            x = node["x"]
            y = node["y"]
            self.add_node(Node(x, y))
            for edge in node["edges"]:
                id = edge["id"]
                id_from = edge["id_from"]
                id_to = edge["id_to"]
                length = edge["length"]
                road_category = edge["road_category"]
                number_of_attractions = edge["number_of_attractions"]
                self.graph[id_from].add_edge(Edge(id, id_from, id_to, length, road_category, number_of_attractions))

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
