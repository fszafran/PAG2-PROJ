import math
from collections import defaultdict

import arcpy

# deklaracja zmiennej globalnej wskazujacej na aktualne id wezla
id_node = 0


class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.neighbours = []
        # self.edge_out = []

    def add_neighbour(self, edge):
        if edge.get_id() not in self.neighbours:
            self.neighbours.append(edge)

    def get_id(self):
        return self.id

    def get_neighbours(self):
        return self.neighbours

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

class Edge:
    def __init__(self, id):
        self.id = id
        self.id_from = None
        self.id_to = None
        self.length = None

    def set_id_from(self, id_from):
        self.id_from = id_from

    def set_id_to(self, id_to):
        self.id_to = id_to

    def set_length(self, length):
        self.length = length

    def get_length(self):
        return self.length

    def get_id(self):
        return self.id

    def get_id_from(self):
        return self.id_from

    def get_id_to(self):
        return self.id_to


def extract_min(Q, d):
    d_min = float('inf')
    index_min = None
    for index in Q:
        if d[index] < d_min:
            d_min = d[index]
            index_min = index
            # print(d_min, " : ", d[index])
    return index_min


def get_neighbouring_nodes_and_distance(node):
    neighbouring_edges = node.get_neighbours()
    neighbouring_nodes_d = []
    # print([edge.get_id() for edge in neighbouring_edges])
    for e in neighbouring_edges:
        # print(f"from: {e.get_id_from()}, to: {e.get_id_to()}, node id: {node.get_id()}")
        if e.get_id_from() == node.get_id():
            neighbouring_nodes_d.append((e.get_id_to(), e.get_length()))
        else:
            neighbouring_nodes_d.append((e.get_id_from(), e.get_length()))

    return neighbouring_nodes_d

def create_index(x, y):
    x = str(round(x))
    y = str(round(y))
    index = x + " " + y
    return index


def add_node_to_dic(index, edge, x, y):
    if index in dic:
        temp_node = dic[index]
        temp_node.add_neighbour(edge)
        # print(f"dodanie sasiada dla wierzcholka: {index} krawedz o id {edge.get_id()}")
        # print(f"lista sasiadow: {[edge.get_id() for edge in temp_node.get_neighbours()]}")
    else:
        node = Node(index, x, y)
        node.add_neighbour(edge)
        dic[index] = node
        # print(f"stworzenie wierzcholka: {index} oraz dodanie pierwszego sasiada {edge.get_id()}")
        # print(f"lista sasiadow: {[edge.get_id() for edge in node.get_neighbours()]}")

dic = defaultdict(Node)
with arcpy.da.SearchCursor("skjz", ["SHAPE@"]) as cursor:
    id_edge = 0
    for row in cursor:
        # reading edge
        geometry = row[0]
        first_point = geometry.firstPoint
        last_point = geometry.lastPoint
        x_f, y_f = first_point.X, first_point.Y
        x_l, y_l = last_point.X, last_point.Y

        # calculating distance
        length = math.sqrt((x_l - x_f) ** 2 + (y_l - y_f) ** 2)

        # creating object Edge
        edge = Edge(id_edge)
        edge.set_length(length)

        # creating index for both points
        index_f = create_index(x_f, y_f)
        index_l = create_index(x_l, y_l)

        # setting id nodes to edge
        edge.set_id_from(index_f)
        edge.set_id_to(index_l)

        # creating obcjects Nodes
        add_node_to_dic(index_f, edge, x_f, y_f)
        add_node_to_dic(index_l, edge, x_l, y_l)

        id_edge += 1
