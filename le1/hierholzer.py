from collections.abc import Sequence

type Edge = tuple[int, int]
type AdjacencyList = dict[int, set[Edge]]


def hierholzer(edges: Sequence[Edge], start: int) -> list[Edge]:
    """
    Hierholzer's algorithm calculates an undirected graph's Eulerian walk by
    constantly starting a walk from the current node to itself while there are
    unused edges.

    Args:
        edges (Sequence[Edge]): The edges of the graph, each edge being a tuple `(u, v)`
            where `u` and `v` are the endpoints of the edge.
        start (int): The node to start the Eulerien walk from. Due to the property of a
            Eulerian walk, a Eulerien walk should be possible regardless of which node
            it starts from.
    
    Returns:
        list[Edge]: The sequence of edges for the Eulerien walk, preserving the endpoint
            order of the edges as they was given.
    """
    adj = make_adjacency_list(edges)
    circuit: list[Edge] = []
    node_stack: list[int] = [start]

    while len(node_stack) > 0:
        current = node_stack[-1]
        if len(adj[current]) > 0:
            edge = adj[current].pop()
            u, v = edge
            other = v if current == u else u
            adj[other].remove(edge)
            node_stack.append(other)
            circuit.append(edge)
        else:
            node_stack.pop()

    return circuit
        

def make_adjacency_list(edges: Sequence[Edge]) -> AdjacencyList:
    adj: AdjacencyList = {}
    for u, v in edges:
        adj.setdefault(u, set()).add((u, v))
        adj.setdefault(v, set()).add((u, v))
    return adj