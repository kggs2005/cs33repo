from collections.abc import Sequence

from utils.union_find import UnionFind


type WeightedEdge = tuple[int, int, int]


def kruskal(edges: Sequence[WeightedEdge]) -> list[WeightedEdge]:
    """
    Kruskal's algorithm is a greedy algorithm used to determine the minimum spanning
    tree of a given graph. It does this by sorting all the edges in increasing order
    of weight, then starting from the lowest-weight edge, starts adding all the edges
    one by one as long as including the edge does not introduce a cycle.

    Union Find is used to check whether two nodes are connected quickly.

    Given a graph with `n` nodes and `e` edges, this algorithm runs in `O(e log e)`
    time (being bottlenecked by the edge sorting) and takes up `O(n + e)` space.

    Args:
        edges (Sequence[WeightedEdge]): The edges of the graph, each edge being a
            tuple `(u, v, w)` where `u` and `v` are the two endpoints and `w` is the
            weight.
    
    Returns:
        list[Edge]: The edges of the resulting MST.
    """
    result: list[WeightedEdge] = []
    union_find = UnionFind()

    for u, v, w in sorted(edges, key=lambda edge: edge[2]): # "edge[2]" is w in (u, v, w)
        if not union_find.in_same_set(u, v):
            union_find.unite(u, v)
            result.append((u, v, w))
    
    return result