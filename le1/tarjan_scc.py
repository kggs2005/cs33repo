from collections.abc import Sequence


type Edge = tuple[int, int]
type AdjacencyList = dict[int, list[int]]


def tarjan_scc(edges: Sequence[Edge]) -> list[list[int]]:
    """
    Tarjan's SCC algorithm is an algorithm that computes a directed graph's strongly
    connected components. It is similar to Kosaraju's algorithm, but it bookkeeps
    information about the DFS, particularly the nodes' discovery time and lowest discovery
    time of any visitable node, allowing it to perform DFS only once unlike Kosaraju's.

    Parameters:
        edges (Sequence[Edge]): The edges of the graph, each edge being a tuple `(u, v)`
            where `u` has an edge directed to `v`.
    
    Returns:
        list[list[int]]: A list of int lists, each int list being a list of the nodes that
            define a strongly connected component.
    """
    adj = make_adjacency_list(edges)

    nodes: set[int] = set()
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)

    discovery_time: dict[int, int] = {}
    lowest_discovery_time_visitable: dict[int, int] = {}

    node_stack: list[int] = []
    nodes_in_stack: set[int] = set()
    all_sccs: list[list[int]] = []
    time = 0

    def get_scc(last_node: int) -> None:
        scc: list[int] = []
        while True:
            current_node = node_stack.pop()
            nodes_in_stack.remove(current_node)
            scc.append(current_node)
            if current_node == last_node:
                break
        all_sccs.append(scc)

    def dfs(current_node: int) -> None:
        nonlocal time
        discovery_time[current_node] = time
        lowest_discovery_time_visitable[current_node] = time
        time += 1

        node_stack.append(current_node)
        nodes_in_stack.add(current_node)

        for neighboring_node in adj[current_node]:
            if neighboring_node not in discovery_time:
                dfs(neighboring_node)
                lowest_discovery_time_visitable[current_node] = min(
                    lowest_discovery_time_visitable[current_node],
                    lowest_discovery_time_visitable[neighboring_node]
                )
            elif neighboring_node in nodes_in_stack:
                lowest_discovery_time_visitable[current_node] = min(
                    lowest_discovery_time_visitable[current_node],
                    discovery_time[neighboring_node]
                )
        
        if lowest_discovery_time_visitable[current_node] == discovery_time[current_node]:
            get_scc(current_node)
    
    for current_node in nodes:
        if current_node not in discovery_time:
            dfs(current_node)

    return all_sccs


def make_adjacency_list(edges: Sequence[Edge]) -> AdjacencyList:
    adj: AdjacencyList = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
    return adj