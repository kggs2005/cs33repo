from collections.abc import Sequence


type Edge = tuple[int, int]
type AdjacencyList = dict[int, list[int]]


def kosaraju(edges: Sequence[Edge]) -> list[list[int]]:
    """
    Kosaraju's algorithm is an algorithm that computes a directed graph's strongly
    connected components. It does this by performing DFS on the directed graph, tracking
    the order of DFS in a stack. Note that the deeper a node is in the DFS operation, the
    higher they are on the stack.
    
    Afterwards, the graph is then reversed and DFS is performed again, starting with
    the deepest nodes. This algorithm posits that any nodes visited by the DFS starting
    at the node at the top of the stack are in the same strongly connected component
    as that node.

    Parameters:
        edges (Sequence[Edge]): The edges of the graph, each edge being a tuple `(u, v)`
            where `u` has an edge directed to `v`.
    
    Returns:
        list[list[int]]: A list of int lists, each int list being a list of the nodes that
            define a strongly connected component.
    """
    adj_normal = _make_adjacency_list(edges)
    node_stack: list[int] = []
    visited: set[int] = set()
    
    nodes: set[int] = set()
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)

    def dfs(current_node: int, adj: AdjacencyList, group: list[int]) -> None:
        visited.add(current_node)
        for neighboring_node in adj[current_node]:
            if neighboring_node not in visited:
                dfs(neighboring_node, adj, group)
        group.append(current_node)

    for current_node in nodes:
        if current_node not in visited:
            dfs(current_node, adj_normal, node_stack)
    
    adj_reverse = _make_adjacency_list([(v, u) for u, v in edges])
    visited.clear()

    all_sccs: list[list[int]] = []
    while len(node_stack) > 0:
        current_node = node_stack.pop()
        if current_node not in visited:
            scc: list[int] = []
            dfs(current_node, adj_reverse, scc)
            all_sccs.append(scc)
    
    return all_sccs


def _make_adjacency_list(edges: Sequence[Edge]) -> AdjacencyList:
    adj: AdjacencyList = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
    return adj