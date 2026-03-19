from typing import Sequence


type WeightedEdge = tuple[int, int, int]


def floyd_warshall(edges: Sequence[WeightedEdge]) -> dict[int, dict[int, int | float]]:
    """
    Floyd-Warshall is an algorithm used to determine the shortest distance from
    any two nodes in a directed graph. It does this by using the recurrence

    `s(k, i, j) = min(s(k - 1, i, j), s(k - 1, i, k) + s(k - 1, k, j))`
    
    where `s(k, i, j)` is the shortest distance between `i` and `j` that uses only
    intermediate nodes that are at most `k`.

    Given a graph with `n` nodes and `e` edges, this algorithm runs in `O(n^3 + e)`
    time and takes up `O(n^2)` space.

    Args:
        edges (Sequence[WeightedEdge]): The edges of the graph, each edge being a
            tuple `(u, v, w)` where `u` and `v` are the two endpoints and `w` is the
            weight.
    
    Returns:
        dict[int,dict[int,int|float]]: A 2-dimensional dictionary of the distances between
        any two nodes. If two nodes are unreachable from each other, then the value is
        `infinity`.
    """
    distance: dict[int, dict[int, int | float]] = {}

    node_set: set[int] = set()
    for u, v, _ in edges:
        node_set.add(u)
        node_set.add(v)
    
    nodes = list(sorted(node_set))

    for i in nodes:
        for j in nodes:
            distance.setdefault(i, {})[j] = float('inf')
        distance[i][i] = 0
    
    for i, j, w in edges:
        distance[i][j] = min(distance[i][j], w)
    
    for k in nodes:
        for i in nodes:
            for j in nodes:
                distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])
    
    return distance