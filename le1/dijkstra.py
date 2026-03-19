from collections.abc import Sequence
from heapq import heappush, heappop


type WeightedEdge = tuple[int, int, int]
type AdjacencyList = dict[int, list[tuple[int, int]]]


def dijkstra(edges: Sequence[WeightedEdge], start: int) -> dict[int, int]:
    """
    Dijkstra's algorithm is used to find the shortest path from a given node to the
    other nodes in a directed graph. It is an adaptation of BFS that uses a minheap
    to keep track of the node with the shortest distance at any point of the algorithm.

    Given a graph with `n` nodes and `e` edges, this algorithm runs in `O(e log e)`
    time and takes up `O(n + e)` space.

    Args:
        edges (Sequence[WeightedEdge]): The edges of the graph, each edge being a
            tuple `(u, v, w)` where `u` and `v` are the two endpoints and `w` is the
            weight.
        start (int): The starting node.
    
    Returns:
        dict[int,int]: A dictionary `d`, where `d[i]` is the distance from `start` to
        `node i`. If `node i` is unreachable from `start`, then `i` will not a key in
        `d`.
    """
    adj = make_adjacency_list(edges)
    distance: dict[int, int] = {}
    visited: set[int] = set()
    node_heap: list[tuple[int, int]] = [(0, start)]

    while len(node_heap) > 0:
        current_distance, current_node = heappop(node_heap)
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        distance[current_node] = current_distance

        for neighbor, neighbor_edge_weight in adj.get(current_node, []):
            heappush(node_heap, (current_distance + neighbor_edge_weight, neighbor))
    
    return distance


def make_adjacency_list(edges: Sequence[WeightedEdge]):
    adj: AdjacencyList = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((v, w))
    return adj