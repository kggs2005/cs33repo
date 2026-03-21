from collections.abc import Sequence


type Edge = tuple[int, int]
type AdjacencyList = dict[int, list[int]]


def find_centroid(edges: Sequence[Edge]) -> int:
    """
    Finds a centroid of the tree defined by the given edges.

    The centroid of a tree is a node such that, if removed, all remaining
    connected components have size at most node_count/2, where node_count is the total number of nodes.

    Parameters:
        edges (Sequence[Edge]): A sequence of undirected edges (current_node, neighboring_node) representing the tree.

    Returns:
        int: The label of one centroid node.

    Raises:
        ValueError: If there are no edges
    """
    if not edges:
        raise ValueError("There are no edges given.")

    adj = make_adjacency_list(edges)
    node_count = len(adj)
    sizes: dict[int, int] = {}
    root = next(iter(adj))

    def dfs(current_node: int, parent: int | None) -> None:
        sizes[current_node] = 1
        for neighboring_node in adj[current_node]:
            if neighboring_node != parent:
                dfs(neighboring_node, current_node)
                sizes[current_node] += sizes[neighboring_node]

    dfs(root, None)

    def find(current_node: int, parent: int | None, centroid: int) -> int:
        max_subtree = 0
        for neighboring_node in adj[current_node]:
            if neighboring_node != parent:
                centroid = find(neighboring_node, current_node, centroid)
                max_subtree = max(max_subtree, sizes[neighboring_node])
        max_subtree = max(max_subtree, node_count - sizes[current_node])
        if max_subtree <= node_count // 2:
            centroid = current_node
        return centroid

    return find(root, None, root)


def make_adjacency_list(edges: Sequence[Edge]) -> AdjacencyList:
    adj: AdjacencyList = {}
    for current_node, neighboring_node in edges:
        adj.setdefault(current_node, []).append(neighboring_node)
        adj.setdefault(neighboring_node, []).append(current_node)
    return adj