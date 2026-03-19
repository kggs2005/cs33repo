from collections.abc import Sequence
from heapq import heappush, heappop


type WeightedEdge = tuple[int, int, int]
type AdjacencyList = dict[int, list[tuple[int, int]]]


def prim(edges: Sequence[WeightedEdge]) -> list[WeightedEdge]:
    """
    Prim's algorithm is a greedy algorithm used to determine the minimum spanning
    tree of an undirected graph. It does this by keeping track of a set of nodes
    (initially containing one arbitrary node), and while not all nodes are connected,
    continues to add therandint64 lowest-weight edge that connects a node in this set
    to a node not in this set and adding the latter node to the set.

    A minheap is used to keep track of the lowest-weight edge at any point of the
    algorithm.

    Given a graph with `n` nodes and `e` edges, this algorithm runs in `O(e log e)`
    time (being bottlenecked by the minheap operations) and takes up `O(n + e)` space.

    Args:
        edges (Sequence[WeightedEdge]): The edges of the graph, each edge being a
            tuple `(u, v, w)` where `u` and `v` are the two endpoints and `w` is the
            weight.
    
    Returns:
        list[Edge]: The edges of the resulting MST.
    """
    adj = make_adjacency_list(edges)
    result: list[WeightedEdge] = []
    edge_heap: list[WeightedEdge] = []

    total_node_count = len(adj.keys())
    start_node = list(adj.keys())[0] # Arbitrary starting node
    connected_nodes = {start_node}

    for v, w in adj[start_node]:
        if v not in connected_nodes:
            heappush(edge_heap, (w, start_node, v))
            # Weight is first in the heappush so that Python's heappush function
            # uses the weight as the basis for the heap operations
    
    edge_set: set[WeightedEdge] = set(edges)

    while len(connected_nodes) < total_node_count:
        w, u, v = heappop(edge_heap)
        # Retain order of endpoints in the original sequence of given edges
        result.append((u, v, w) if (u, v, w) in edge_set else (v, u, w))
        connected_nodes.add(v)

        for v_neighbor, v_neighbor_edge_weight in adj[v]:
            if v_neighbor not in connected_nodes:
                heappush(edge_heap, (v_neighbor_edge_weight, v, v_neighbor))
    
    return result


def make_adjacency_list(edges: Sequence[WeightedEdge]) -> AdjacencyList:
    adj: AdjacencyList = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))
    return adj