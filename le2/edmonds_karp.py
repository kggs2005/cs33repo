from collections.abc import Sequence
from collections import deque


type WeightedEdge = tuple[int, int, int]
type AdjacencyList = dict[int, list[_FlowEdge]]


class _FlowEdge:
    """
    Internal class representing a directed edge in the flow network.

    Each edge has:
      - a source node
      - a destination node
      - a capacity (maximum possible flow)
      - a current flow value
      - a reverse edge (used to maintain residual capacities)

    Reverse edges are automatically created with zero capacity.
    """
    def __init__(self, source: int, destination: int, capacity: int, reverse: _FlowEdge | None=None) -> None:
        self._source = source
        self._destination = destination
        self.flow = 0
        self._capacity = capacity
        self._reverse = reverse or _FlowEdge(destination, source, 0, self)
    
    @property
    def source(self) -> int:
        """The source of this edge."""
        return self._source
    
    @property
    def destination(self) -> int:
        """The destination of this edge."""
        return self._destination

    @property
    def capacity(self) -> int:
        """The capacity of this edge."""
        return self._capacity
    
    @property
    def reverse(self) -> _FlowEdge:
        """The reverse of this edge, used for augmenting paths."""
        return self._reverse
    
    @property
    def residual(self) -> int:
        """
        Return the residual capacity of this edge.

        `residual` = `capacity` - `flow`
        """
        return self.capacity - self.flow


def edmonds_karp(edges: Sequence[WeightedEdge], source: int, sink: int) -> tuple[int, list[WeightedEdge]]:
    """
    Edmonds-Karp algorithm looks for the maximum flow from `source` to `sink` in a directed
    graph well as determine the cheapest total cost to cut the flow from `source` to `sink`
    by continuing to augment paths until no such flow exists anymore.

    This algorithm runs in both O(ne^2) and O(nk) where `n` is the number of nodes, `e`
    is the number of edges, and `k` is the number of augmentations.

    Parameters:
        edges (Sequence[WeightedEdge]): The edges of the graph, where each edge is a tuple
            `(u, v, w)` such that an edge of capacity `w` connects from `u` to `v`.
        source (int): The node where the flow starts.
        sink (int): The node where the flow ends.
    
    Returns:
        tuple[int,list[WeightedEdge]]:
            - The maximum flow from `source` to `sink`
            - The list of edges that form the minimum cut separating `source` from `sink`.
    """
    flow_edges = [_FlowEdge(u, v, w) for u, v, w in edges]
    adj: AdjacencyList = {}
    for flow_edge in flow_edges:
        adj.setdefault(flow_edge.source, []).append(flow_edge)
        adj.setdefault(flow_edge.destination, []).append(flow_edge.reverse)

    def augmenting_path() -> list[_FlowEdge] | None:
        visited: set[int] = set()
        node_queue: deque[int] = deque()
        previous: dict[int, _FlowEdge] = {}
        visited.add(source)
        node_queue.append(source)

        while len(node_queue) > 0:
            current_node = node_queue.popleft()

            if current_node == sink:
                path: list[_FlowEdge] = []
                while current_node != source:
                    path.append(previous[current_node])
                    current_node = previous[current_node].source
                return path[::-1]
            
            for neighboring_edge in adj[current_node]:
                if neighboring_edge.residual > 0 and neighboring_edge.destination not in visited:
                    visited.add(neighboring_edge.destination)
                    previous[neighboring_edge.destination] = neighboring_edge
                    node_queue.append(neighboring_edge.destination)
        
        return None
    
    # Max-Flow
    total_flow = 0

    while (path := augmenting_path()) is not None:
        added_flow = min(flow_edge.residual for flow_edge in path)
        assert added_flow > 0
        total_flow += added_flow

        for flow_edge in path:
            flow_edge.flow += added_flow
            flow_edge.reverse.flow -= added_flow
    
    # Min-Cut
    visited: set[int] = set()
    node_queue: deque[int] = deque()
    visited.add(source)
    
    while len(node_queue) > 0:
        current_node = node_queue.popleft()
        for neighboring_edge in adj[current_node]:
            if neighboring_edge.residual > 0 and neighboring_edge.destination not in visited:
                visited.add(neighboring_edge.destination)
                node_queue.append(neighboring_edge.destination)

    min_cut_edges: list[WeightedEdge] = []
    for node in visited:
        for flow_edge in adj[node]:
            if flow_edge.capacity > 0 and flow_edge.destination not in visited:
                min_cut_edges.append((flow_edge.source, flow_edge.destination, flow_edge.capacity))

    return total_flow, min_cut_edges