from collections.abc import Sequence


type Edge = tuple[int, int]
type AdjacencyList = dict[int, list[int]]


def kuhn(edges: Sequence[Edge]) -> list[Edge]:
    """
    Kuhn's algorithm is an algorithm that finds the maximum matching for a
    bipartite graph. It does this by continuously rematching alternating
    left and right until a node cannot find another match.

    Parameters:
        edges (Sequence[Edge]): The edges of the bipartite graph, where
            each edge is a tuple `(l, r)` where `l` is a node in the left
            graph and `r` is a node in the right graph.
    
    Returns:
        list[Edge]: The list of edges in the maximum matching, where each
            edge is a tuple `(l, r)` where `l` is a node in the left
            graph and `r` is a node in the right graph.
    """
    if len(edges) == 0:
        return []

    adj = _make_adjacency_list(edges)
    left_partner: dict[int, int] = {} # A match would be (left_partner[r], r)
    visited: set[int] = set()

    def try_match(left: int):
        if left not in visited:
            visited.add(left)
            for right in adj[left]:
                if right not in left_partner or try_match(left_partner[right]):
                    left_partner[right] = left
                    return True
        return False
    
    size = 0
    for left in adj.keys():
        visited.clear()
        if try_match(left):
            size += 1

    matches = [(v, k) for k, v in left_partner.items()]
    assert len(matches) == size
    return matches


def _make_adjacency_list(edges: Sequence[Edge]) -> AdjacencyList:
    adj: AdjacencyList = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
    return adj