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


def dijkstra(first_node_id, last_node_id, nodes):
    S = set()
    Q = {}
    p = {}
    d = {}

    for index, node in nodes.items():
        d[index] = float('inf')
        p[index] = -1
        Q[index] = node

    d[first_node_id] = 0
    # Q[first_node_id] = nodes[first_node_id]

    while Q:
        # searching for closest node
        current_id = extract_min(Q, d)
        # print("current_id -> ", current_id)

        # checking if we got the ending node
        # print(current_id, last_node_id)
        if current_id == last_node_id:
            break

        # adding new node id to S
        S.add(current_id)
        del Q[current_id]

        # recreating object Node to get neighbours (edges)
        current_node = nodes[current_id]

        # based on neighbouring edges getting neighbouring nodes and length
        neighbouring_nodes_and_distance = get_neighbouring_nodes_and_distance(current_node)
        for neighbour_id, length in neighbouring_nodes_and_distance:
            # print(neighbour_id)
            if neighbour_id in S:
                continue
            if d[neighbour_id] > d[current_id] + length:
                d[neighbour_id] = d[current_id] + length
                p[neighbour_id] = current_id

    return p


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


def reconstruct_path(first_node_id, last_node_id, p):
    path = []
    current_id = last_node_id

    while current_id != -1:  # Dopóki mamy poprzednika
        path.append(current_id)
        current_id = p[current_id]

        # Jeśli dotarliśmy do węzła początkowego, zatrzymujemy się
        if current_id == first_node_id:
            path.append(first_node_id)
            break

    # Odwracamy kolejność, aby ścieżka była od startu do końca
    path.reverse()

    return path


def add_path_to_feature_class(path, output_fc, nodes):
    # Tworzymy linię na podstawie kolejnych punktów w ścieżce
    with arcpy.da.InsertCursor(output_fc, ["SHAPE@"]) as cursor:
        array = arcpy.Array()
        for node_id in path:
            # Pobieramy współrzędne dla `node_id` (np. z twojego słownika `nodes`)
            x, y = nodes[node_id].get_x(), nodes[node_id].get_y()
            point = arcpy.Point(x, y)
            array.add(point)

        # Tworzymy polilinię z punktów i dodajemy do warstwy
        polyline = arcpy.Polyline(array)
        cursor.insertRow([polyline])


def create_line_feature_class(output_fc, spatial_reference):
    arcpy.management.CreateFeatureclass(
        out_path=output_fc.rsplit('\\', 1)[0],
        out_name=output_fc.rsplit('\\', 1)[-1],
        geometry_type="POLYLINE",
        spatial_reference=spatial_reference
    )


arcpy.env.workspace = r"C:\Users\mikol\Desktop\PAG\MyProject1\MyProject1.gdb"
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


pathway = dijkstra("471020 572970", "472078 573637", dic)
reconstructed = reconstruct_path("471020 572970", "472078 573637", pathway)

output_fc = r"C:\Users\mikol\Desktop\PAG\MyProject1\MyProject1.gdb\path_layer"  # Ścieżka do nowej warstwy
spatial_reference = arcpy.SpatialReference(2180)
create_line_feature_class(output_fc, spatial_reference)
add_path_to_feature_class(reconstructed, output_fc, dic)
print("Warstwa liniowa utworzona pomyślnie.")