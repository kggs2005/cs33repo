from collections.abc import Sequence
from math import ceil, log2


type Edge = tuple[int, int]
type AdjacencyList = dict[int, list[_LCANode]]


class LCAFinder:
    """
    Data structure that can find the least common ancestor (LCA) of any two nodes
    using binary lifting, allowing it to have `O(n log n)` preprocessing time and
    `O(log n)` query time.

    Parameters:
        edges (Sequence[Edge]): A sequence of undirected edges `(u, v)` representing
            the tree.
        root (int): The label of the root node of the tree.

    Raises:
        ValueError: If the given `root` is not present in the tree.
    """
    def __init__(self, edges: Sequence[Edge], root: int) -> None:
        self.nodes: dict[int, _LCANode] = {}
        for u, v in edges:
            self.nodes.setdefault(u, _LCANode(u))
            self.nodes.setdefault(v, _LCANode(v))
        
        if root not in self.nodes:
            raise ValueError(f"Given root {root} is not in the tree.")
        
        self._root = self.nodes[root]
        self._height = ceil(log2(len(self.nodes)))

        for u, v in edges:
            self.nodes[u].adjacent_nodes.append(self.nodes[v])
            self.nodes[v].adjacent_nodes.append(self.nodes[u])
        
        def dfs(current_node: _LCANode, parent: _LCANode, depth: int) -> None:
            current_node.depth = depth
            for neighboring_node in current_node.adjacent_nodes:
                if neighboring_node is not parent:
                    neighboring_node.parent = current_node
                    dfs(neighboring_node, current_node, depth + 1)
        
        dfs(self._root, self._root, 0)

        for node in self.nodes.values():
            node.ancestors[0] = node.parent
        for k in range(1, self._height + 1):
            for node in self.nodes.values():
                parent = node.ancestors.get(k - 1, node)
                node.ancestors[k] = parent.ancestors.get(k - 1, parent)
    
    def least_common_ancestor(self, u: int, v: int) -> int:
        """
        Returns the least common ancestor (LCA) of nodes `u` and `v`.

        Parameters:
            u (int): The label of the first node.
            v (int): The label of the second node.

        Returns:
            int: The label of the least common ancestor node.

        Raises:
            KeyError: If either `u` or `v` is not present in the tree.
        """
        if u not in self.nodes:
            raise KeyError(f"Given node {u} is not in the tree.")
        if v not in self.nodes:
            raise KeyError(f"Given node {v} is not in the tree.")

        node_u = self.nodes[u]
        node_v = self.nodes[v]
        
        if node_u.depth > node_v.depth:
            node_u = self._climb(node_u, node_u.depth - node_v.depth)
        elif node_v.depth > node_u.depth:
            node_v = self._climb(node_v, node_v.depth - node_u.depth)

        if node_u is node_v:
            return node_u.label

        for k in range(self._height, -1, -1):
            if node_u.ancestors.get(k, node_u) is not node_v.ancestors.get(k, node_v):
                node_u = node_u.ancestors.get(k, node_u)
                node_v = node_v.ancestors.get(k, node_v)
        
        return node_u.parent.label
    
    def _climb(self, node: _LCANode, levels: int) -> _LCANode:
        """
        Moves a node up the tree by a given number of `levels` using binary lifting.

        Parameters:
            node (_LCANode): The node to climb from.
            levels (int): The number of levels to climb.

        Returns:
            _LCANode: The ancestor node after climbing the specified number of levels.
        """
        for k in range(self._height, -1, -1):
            if levels >= 1 << k:
                levels -= 1 << k
                node = node.ancestors.get(k, node)
        
        assert levels <= 0
        return node
        

class _LCANode:
    """
    Represents a node in the tree used for LCA computation.
    """
    def __init__(self, label: int) -> None:
        self._label = label
        self.depth = 0
        self.parent = self
        self.adjacent_nodes: list[_LCANode] = []
        self.ancestors: dict[int, _LCANode] = {}
    
    @property
    def label(self) -> int:
        """The label of the node."""
        return self._label
    