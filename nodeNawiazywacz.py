# def find_closest_node2(x_start, y_start, graph):
#     y, x = round(x_start), round(y_start)
#     i = 0
#     steps_to_take = 1
#     current_direction_steps = 0
#     directions = [(1, 0), (0, 1), (-1, 0), (0, -1)] 

#     while True:
#         dx, dy = directions[i % 4]
#         x += dx
#         y += dy

#         key = f"{x}_{y}"
#         if key in graph.graph.keys():
#             return [x, y]
        
#         current_direction_steps += 1
#         if current_direction_steps == steps_to_take:
#             current_direction_steps = 0
#             i += 1
#             if i % 2 == 0:
#                 steps_to_take += 1

# def create_closest_point(y_start, x_start, first_node, second_node, roads):
    
#     def calculate_slope(x1, y1, x2, y2):
#         return (y2 - y1) / (x2 - x1)
    
#     def distance_from_point_to_line(x0, y0, point1, point2):
#         x1, y1 = point1
#         x2, y2 = point2
#         m = calculate_slope(x1, y1, x2, y2)
#         b = y1 - m * x1
#         return abs(m * x0 - y0 + b) / math.sqrt(m ** 2 + 1)
    
#     def closest_point_on_line(x0, y0, x1, y1, m):
#         x_proj = x0 - ((x0 - x1) * m + (y0 - y1)) / (1 + m ** 2)
#         y_proj = y0 + m * (x0 - x_proj)
#         return x_proj, y_proj

#     key_road1 = f"{first_node}_{second_node}"
#     key_road2 = f"{second_node}_{first_node}"
#     if key_road1 in roads:
#         whole_edge = roads[key_road1]
#         print(whole_edge, "->1")
#     elif key_road2 in roads:
#         whole_edge = roads[key_road2]
#         print(whole_edge, "->2")
#     else:
#         print("nie znalazlo")
    
#     min_distance = 9999999999999
#     #x1, y1, x2, y2 = None
#     for i in range(len(whole_edge) - 1):
#         point1 = whole_edge[i]
#         point2 = whole_edge[i + 1]
#         dist = distance_from_point_to_line(x_start, y_start, point1, point2)
#         print(dist)
#         if dist<min_distance:
#             min_distance = dist
#             x1, y1 = point1
#             x2, y2 = point2
#             print("znalezione: ", min_distance)
#     m = calculate_slope(x1, y1, x2, y2)
#     point0 = closest_point_on_line(x_start, y_start, x1, y1, m)

#     cs2180 = CRS.from_proj4(
#         "+proj=tmerc +lat_0=0 +lon_0=19 +k=0.9993 +x_0=500000 +y_0=-5300000 +ellps=GRS80 +units=m +no_defs +type=crs")
#     cs4326 = CRS.from_epsg(4326)
#     transformer = Transformer.from_crs(cs2180, cs4326)
#     point0 = translate_path_part_to_leaflet(point0, transformer)
#     print(point0)
#     return point0