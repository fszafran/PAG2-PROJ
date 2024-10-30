import arcpy

class Edge:
    def __init__(self, id, id_from, id_to, length):
        self.id = id
        self.id_from = id_from
        self.id_to = id_to
        self.length = length

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
            reversed_edge = Edge(edge.id, edge.id_to, edge.id_from, edge.length)
            self.graph[edge.id_to].add_edge(reversed_edge)

    def __repr__(self):
        for key, value in self.graph.items():
            print(f"{key}: {value.edges}")
            
arcpy.env.workspace = r"C:\Users\filo1\Desktop\szkola_sem5\PAG2\proj1\dane\torun\drogi"
arcpy.env.overwriteOutput = True

graph = Graph()
drogiTorun = arcpy.ListFeatureClasses("*.shp")
print(drogiTorun)

for featureClass in drogiTorun:
    with arcpy.da.SearchCursor(featureClass, ["SHAPE@"]) as cursor:
        for i, row in enumerate(cursor):
            geometry = row[0]
            length = geometry.length
            firstX = round(geometry.firstPoint.X)
            firstY = round(geometry.firstPoint.Y)
            lastX = round(geometry.lastPoint.X)
            lastY = round(geometry.lastPoint.Y)

            firstNode = Node(firstX, firstY)
            lastNode = Node(lastX, lastY)

            graph.add_node(firstNode)
            graph.add_node(lastNode)

            edge = Edge(i, firstNode.id, lastNode.id, length)
            graph.add_edge(edge)

print(graph)