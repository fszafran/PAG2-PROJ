import arcpy
from HelperClasses import *
import time
from algorithm import algorithm

def prepare_data(kopia_drogi_torun, atrakcje):
    """
    1. Tworzymy buffera dla dróg
    2. Spatial join łączy warstwy jeżeli punkty mają styczność z bufferami, 
    przy okazji generuje pole Join_Count z liczbą punktow w bufferze
    3. Łączymy warstwy po ID1 i dodajemy join count do drog (warto działać na kopii warstwy)
    """
    bufferedDrogi = arcpy.analysis.Buffer(kopia_drogi_torun, "bufferedDrogi.shp", "25 meters", dissolve_option="NONE", dissolve_field=None, method="PLANAR")
    joined = arcpy.analysis.SpatialJoin(bufferedDrogi, atrakcje, "attractions_near_roads", "JOIN_ONE_TO_ONE", "KEEP_ALL", None, "INTERSECT")
    arcpy.management.JoinField(kopia_drogi_torun, "ID1", joined, "ID1", ["Join_Count"])
    return kopia_drogi_torun

def calculate_attraction_weights(attraction_counts: Set[int]) -> Dict[int, int]:
    weighted_attractions = {}
    sorted_counts = sorted(attraction_counts, reverse=True)
    for i, count in enumerate(sorted_counts):
        weighted_attractions[count] = i + 1
    return weighted_attractions

def generate_graph(warstwa_drog) -> Graph:
    graph = Graph()
    attraction_counts = set()

    with arcpy.da.SearchCursor(warstwa_drog, ["Join_Count"]) as cursor:
        for row in cursor:
            attraction_counts.add(row[0])
    weighted_attractions: Dict[int, int] = calculate_attraction_weights(attraction_counts)

    with arcpy.da.SearchCursor(warstwa_drog, ["SHAPE@", "Join_Count", "klasaDrogi"]) as cursor:
        for i, row in enumerate(cursor):
            geometry = row[0]
            attraction_number = weighted_attractions[row[1]] # im wiecej atrakcji tym mniejsza waga/koszt
            klasa_drogi = CategoryFactory.get_category(row[2]).value # zwroci predkosc przyjeta dla danej kategorii drogi
            length = geometry.length
            
            firstX = round(geometry.firstPoint.X)
            firstY = round(geometry.firstPoint.Y)
            lastX = round(geometry.lastPoint.X)
            lastY = round(geometry.lastPoint.Y)

            firstNode = Node(firstX, firstY)
            lastNode = Node(lastX, lastY)

            graph.add_node(firstNode)
            graph.add_node(lastNode)

            edge = Edge(i, firstNode.id, lastNode.id, length, klasa_drogi, attraction_number)
            graph.add_edge(edge)
    return graph


if __name__ == "__main__":
    start = time.time()
    arcpy.env.workspace = r"C:\Users\filo1\Desktop\szkola_sem5\PAG2\proj1\arcgis_proj\MyProject.gdb"
    arcpy.env.overwriteOutput = True

    atrakcjeLayer = arcpy.ListFeatureClasses("attr*")[0]
    drogi_torun = arcpy.ListFeatureClasses("L4*")[0]

    # kopia_drogi_torun = arcpy.management.CopyFeatures(drogi_torun, "kopia_drogi_torun")
    # kopia_drogi_torun = prepare_data(kopia_drogi_torun, atrakcjeLayer)

    graph = generate_graph(drogi_torun)
    print(algorithm(graph, [476023, 573797], [479470, 573184], 1))
    end = time.time()
    print(end - start)