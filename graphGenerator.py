import arcpy
from HelperClasses import Node, Edge, Graph
import time

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

def generate_graph(warstwa_drog):
    graph = Graph()
    with arcpy.da.SearchCursor(warstwa_drog, ["SHAPE@", "Join_Count"]) as cursor:
        for i, row in enumerate(cursor):
            geometry = row[0]
            attraction_number = row[1]
            length = geometry.length
            firstX = round(geometry.firstPoint.X)
            firstY = round(geometry.firstPoint.Y)
            lastX = round(geometry.lastPoint.X)
            lastY = round(geometry.lastPoint.Y)

            firstNode = Node(firstX, firstY)
            lastNode = Node(lastX, lastY)

            graph.add_node(firstNode)
            graph.add_node(lastNode)

            edge = Edge(i, firstNode.id, lastNode.id, length, attraction_number)
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
    
    print(graph.graph)
    end = time.time()
    print(end - start)