import numpy as np
from HelperClasses import *
from typing import List, Dict
from queue import PriorityQueue
from collections import defaultdict

def heuristic(from_node_id: str, to_node_id: str) -> float:
    x1, y1 = map(float, from_node_id.split("_"))
    x2, y2 = map(float, to_node_id.split("_"))
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def reconstruct_path(came_from: Dict[str, str], current_node: Node) -> List[Node]:
    path = [current_node]
    while current_node.id in came_from:
        current_node= came_from[current_node.id]
        path.append(current_node)
    path.reverse()
    return path

def algorithm(graph: Graph, start: List[float], end: List[float], route_type: int) -> List[Node]:
    start_node = graph.graph[Node(start[0], start[1]).id]
    end_node = graph.graph[Node(end[0], end[1]).id]

    open_set = PriorityQueue()
    open_set.put((0, start_node))

    came_from = {}
    g_score = defaultdict(lambda: float("inf"))
    g_score[start_node.id] = 0

    f_score = defaultdict(lambda: float("inf"))
    f_score[start_node.id] = heuristic(start_node.id, end_node.id)

    open_set_hash = {start_node.id}

    while not open_set.empty():
        current_node: Node = open_set.get()[1] # jezeli przetworzony, pass

        if current_node.id not in open_set_hash:
            continue

        open_set_hash.remove(current_node.id)

        if current_node.id == end_node.id:
            return reconstruct_path(came_from, current_node)

        neighbours = current_node.get_neighbours()
        for edge, neighbour_id in neighbours:
            temp_g_score = g_score[current_node.id] + edge.get_appropriate_cost(route_type)
            if temp_g_score < g_score[neighbour_id]:
                came_from[neighbour_id] = current_node
                g_score[neighbour_id] = temp_g_score
                f_score[neighbour_id] = temp_g_score + heuristic(graph.graph[neighbour_id].id, end_node.id)
                if neighbour_id not in open_set_hash:
                    open_set.put((f_score[neighbour_id], graph.graph[neighbour_id]))
                    open_set_hash.add(neighbour_id)
    return []  
  
    
    