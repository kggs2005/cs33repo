from collections.abc import Sequence


type WeightedEdge = tuple[int, int, int]


def kruskal(edges: Sequence[WeightedEdge]) -> list[WeightedEdge]:
    """
    Kruskal's algorithm is a greedy algorithm used to determine the minimum spanning
    tree of an undirected graph. It does this by sorting all the edges in increasing
    order of weight, then starting from the lowest-weight edge, starts adding all the
    edges one by one as long as including the edge does not introduce a cycle.

    Union Find is used to check whether two nodes are connected quickly.

    Given a graph with `n` nodes and `e` edges, this algorithm runs in `O(e log e)`
    time (being bottlenecked by the edge sorting) and takes up `O(n + e)` space.

    Parameters:
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


class UnionFind:
    class Node:
        def __init__(self, label: int):
            self._label = label
            self.parent = self
            self.rank = 0

        @property
        def label(self) -> int:
            return self._label

    def __init__(self):
        self._nodes: dict[int, UnionFind.Node] = {}
    
    def unite(self, i: int, j: int) -> bool:
        node_i = self._nodes.setdefault(i, UnionFind.Node(i))
        node_j = self._nodes.setdefault(j, UnionFind.Node(j))
        root_i = self._get_root(node_i)
        root_j = self._get_root(node_j)

        if root_i == root_j:
            return False
        
        if root_i.rank < root_j.rank:
            root_i.parent = root_j
        elif root_i.rank > root_j.rank:
            root_j.parent = root_i
        else:
            root_j.parent = root_i
            root_i.rank += 1

        return True

    def in_same_set(self, i: int, j: int) -> bool:
        if i not in self._nodes or j not in self._nodes:
            return False
        return self._get_root(self._nodes[i]) == self._get_root(self._nodes[j])
    
    def _get_root(self, node: UnionFind.Node) -> UnionFind.Node:
        if node.parent is not node:
            node.parent = self._get_root(node.parent) 
        return node.parent