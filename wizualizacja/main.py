from algorithm import algorithm
from pyproj import CRS, Transformer
import math

def heuristic(from_node_id: str, to_node_id: str) -> float:
    x1, y1 = map(float, from_node_id.split("_"))
    x2, y2 = map(float, to_node_id.split("_"))
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def calculate_path(graph, x_start, y_start, x_end, y_end, route_type):
    start = [x_start, y_start]
    end = [x_end, y_end]
    path = algorithm(graph, start, end, heuristic, route_type)
    return path

def find_closest_node(x_start, y_start, graph):
    y, x = round(x_start), round(y_start)
    i = 0
    while True:
        for _ in range(0,(i//2)+1):
            if i % 4 == 0:
                x+=1
            elif i % 4 ==1:
                y += 1
            elif i % 4 == 2:
                x-=1
            else:
                y-=1
            key = f"{x}_{y}"
            if key in graph.graph.keys():
                return [x, y]
        i+=1

def get_path_parts(path, drogi):
    cs2180 = CRS.from_proj4(
        "+proj=tmerc +lat_0=0 +lon_0=19 +k=0.9993 +x_0=500000 +y_0=-5300000 +ellps=GRS80 +units=m +no_defs +type=crs")
    cs4326 = CRS.from_epsg(4326)
    transformer = Transformer.from_crs(cs2180, cs4326)
    path_parts = []

    for i in range(len(path) - 1):
        first_node = path[i]
        second_node = path[i + 1]
        key1 = f"{first_node.id}_{second_node.id}"
        key2 = f"{second_node.id}_{first_node.id}"

        if key1 in drogi:
            path_part = drogi[key1]
            translated_path_part = [translate_path_part_to_leaflet(part, transformer) for part in path_part]
            path_parts.append(translated_path_part)
        elif key2 in drogi:
            path_part = drogi[key2]
            translated_path_part = [translate_path_part_to_leaflet(part, transformer) for part in path_part]
            path_parts.append(translated_path_part)
        else:
            raise KeyError(f"Neither {key1} nor {key2} found in drogi")
    return path_parts
    
def translate_path_part_to_leaflet(path_part, transformer):
    x = path_part[0]
    y = path_part[1]
    x, y = transformer.transform(x, y)
    return [x, y]
        


