from collections.abc import Sequence


type WeightedEdge = tuple[int, int, int]


class NegativeCycleError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


def bellman_ford(edges: Sequence[WeightedEdge], start: int) -> dict[int, int | float]:
    """
    Bellman-Ford algorithm, like Dijkstra's algorithm, finds the shortest distance of
    a given node to all other nodes, but can also detect negative cycles. It does this
    by "augmenting" repeatedly using the recurrence

    `d[i] <= d[j] + c`

    where `(i, j, c)` is a directed edge in the graph, and `d[i]` is the distance of
    `node i` from the starting node.
    
    Since a shortest path can only traverse at most the number of nodes in the graph,
    if the graph continues to be augmented past that many augmentations, there must be
    a negative cycle in the graph. Raises a `NegativeCycleError` if such occurs.

    Given a graph with `n` nodes and `e` edges, this algorithm runs in `O(ne)` time and
    takes up `O(n + e)` space.

    Args:
        edges (Sequence[WeightedEdge]): The edges of the graph, each edge being a
            tuple `(u, v, w)` where `u` and `v` are the two endpoints and `w` is the
            weight.
        start (int): The starting node.
    
    Returns:
        dict[int,int]: A dictionary `d`, where `d[i]` is the distance from `start` to
        `node i`. If `node i` is unreachable from `start`, then `d[i]` returns infinity.
    """
    nodes: set[int] = set()
    for u, v, _ in edges:
        nodes.add(u)
        nodes.add(v)
    
    distance: dict[int, int | float] = {i: float('inf') for i in nodes}
    distance[start] = 0

    def augment() -> bool:
        augmented = False
        for i, j, c in edges:
            if distance[j] > distance[i] + c:
                distance[j] = distance[i] + c
                augmented = True
        return augmented

    for _ in range(len(nodes)):
        if not augment():
            return distance

    raise NegativeCycleError("The given graph has a negative cycle!")