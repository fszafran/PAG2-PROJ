import arcpy
from HelperClasses import *
import time
from algorithm import algorithm
import geopandas as gpd
import json
from typing import Set

def prepare_data(kopia_drogi_torun, atrakcje):
    bufferedDrogi = arcpy.analysis.Buffer(kopia_drogi_torun, "bufferedDrogi.shp", "25 meters", dissolve_option="NONE", dissolve_field=None, method="PLANAR")
    joined = arcpy.analysis.SpatialJoin(bufferedDrogi, atrakcje, "attractions_near_roads", "JOIN_ONE_TO_ONE", "KEEP_ALL", None, "INTERSECT")
    arcpy.management.JoinField(kopia_drogi_torun, "ID1", joined, "ID1", ["Join_Count"])
    return kopia_drogi_torun

def calculate_attraction_weights(attraction_counts: Set[int], max_length: float) -> Dict[int, int]:
    weighted_attractions = {}
    sorted_counts = sorted(attraction_counts, reverse=True)
    for i, count in enumerate(sorted_counts):
        weighted_attractions[count] = i + 1 + int(max_length)
    return weighted_attractions

def generate_graph(warstwa_drog) -> Graph:
    graph = Graph()
    attraction_counts = set()
    max_length = 0
    with arcpy.da.SearchCursor(warstwa_drog, ["Join_Count", "SHAPE@"]) as cursor:
        for row in cursor:
            geometry = row[1]
            attraction_counts.add(row[0])
            max_length = max(max_length, geometry.length)
    weighted_attractions: Dict[int, int] = calculate_attraction_weights(attraction_counts, max_length)

    with arcpy.da.SearchCursor(warstwa_drog, ["SHAPE@", "Join_Count", "klasaDrogi"]) as cursor:
        for i, row in enumerate(cursor):
            geometry = row[0]
            # print("attr:", row[1])
            # print("waga:",  weighted_attractions[row[1]])
            attraction_number = weighted_attractions[row[1]] # im wiecej atrakcji tym mniejsza waga/koszt
            spd_limit = CategoryFactory.get_category(row[2]).value # zwroci predkosc przyjeta dla danej kategorii drogi
            length = geometry.length
            
            firstX = geometry.firstPoint.X
            firstY = geometry.firstPoint.Y
            lastX = geometry.lastPoint.X
            lastY = geometry.lastPoint.Y
            
            firstNode = Node(firstX, firstY)
            lastNode = Node(lastX, lastY)

            graph.add_node(firstNode)
            graph.add_node(lastNode)

            edge = Edge(i, firstNode.id, lastNode.id, length, spd_limit, attraction_number)
            graph.add_edge(edge)
    return graph

def connect_to_db(): 
    pass
def roads_to_JSON(warstwa_drog: str) -> None:
    json_dict = {}
    gdf = gpd.read_file(warstwa_drog)
    for _, row in gdf.iterrows():
        geometry= row["geometry"]
        firstX, firstY = geometry.coords[0]
        firstX = round(firstX)
        firstY = round(firstY)

        lastX, lastY = geometry.coords[-1]
        lastX = round(lastX)
        lastY = round(lastY)

        key = f"{firstX}_{firstY}_{lastX}_{lastY}"
        json_dict[key] = list(geometry.coords)
    with open("roads.json", "w") as f:
        json.dump(json_dict, f, indent=4)
    
if __name__ == "__main__":
    start = time.time()
    arcpy.env.workspace = r"C:\Users\filo1\Desktop\szkola_sem5\PAG2\proj1\arcgis_proj\MyProject.gdb"
    arcpy.env.overwriteOutput = True

    # atrakcjeLayer = arcpy.ListFeatureClasses("attr*")[0]
    # drogi_torun = arcpy.ListFeatureClasses("L4*")[0]

    # # kopia_drogi_torun = arcpy.management.CopyFeatures(drogi_torun, "kopia_drogi_torun")
    # # kopia_drogi_torun = prepare_data(kopia_drogi_torun, atrakcjeLayer)
    graph = generate_graph("kopia_drogi_torun")

    URI = "bolt://localhost:7687"
    AUTH = ("neo4j", "69mtdew420")
    graph.to_neo4j(URI, AUTH, "siecdrogowa")

    #graph.to_JSON("graph.json")
    # roads_to_JSON(r"drogi_shp\kopia_drogi_torun.shp")
    # roads_to_JSON(r"drogi_shp\kopia_drogi_torun.shp")
    # print(algorithm(graph, [476023, 573797], [479470, 573184], 1))
    # graph = Graph("graph.json")
    end = time.time()
    print(end - start)