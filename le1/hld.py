from collections.abc import Sequence

from le1.lca import LCAFinder
from utils.segment_tree import SegmentTree


class HLD:
    """
    Heavy-Light Decomposition (HLD) breaks down a tree into heavy paths, where a path starts from
    some head and goes through its largest children all the way to the leaf. This way, the number
    of heavy paths if at most `O(log n)`, where `n` is the number of nodes in the tree.

    This is useful as now range queries, such as segment trees can now be done on trees, and they
    would still run in `O(log n)` time.

    This HLD has the following operations and their respective time complexities:
        - Initialization: `O(n)`
        - `query_sum`: `O(log n)`
        - `query_min`: `O(log n)`
        - `query_max`: `O(log n)`
        - `query_lca`: `O(log n)`
    """
    class Node:
        """Represents a node in the HLD class."""
        def __init__(self, label: int, value: int) -> None:
            self._label = label
            self.value = value
            self.parent: HLD.Node | None = None
            self.depth = 0
            self.size = 0
            self.heavy: HLD.Node | None = None
            self.head: HLD.Node | None = None
            self.pos = -1
            self.adjacent_nodes: list[HLD.Node] = []

        @property
        def label(self) -> int:
            return self._label

    def __init__(self, values: dict[int, int], edges: Sequence[tuple[int, int]], root: int) -> None:
        self.nodes: dict[int, HLD.Node] = {}
        for node_u, node_v in edges:
            self.nodes.setdefault(node_u, HLD.Node(node_u, values.get(node_u, 0)))
            self.nodes.setdefault(node_v, HLD.Node(node_v, values.get(node_v, 0)))

        if root not in self.nodes:
            raise ValueError(f"Given root {root} is not in the tree.")

        self.root = self.nodes[root]

        for node_u, node_v in edges:
            self.nodes[node_u].adjacent_nodes.append(self.nodes[node_v])
            self.nodes[node_v].adjacent_nodes.append(self.nodes[node_u])

        self._dfs(self.root, None, 0)

        self.current_pos = 0
        self._decompose(self.root, self.root)

        n = len(self.nodes)
        self.base_array = [0] * n
        for node in self.nodes.values():
            self.base_array[node.pos] = node.value

        def add(a: int, b: int) -> int:
            return a + b

        self._seg_sum = SegmentTree(self.base_array, add, 0)
        self._seg_min = SegmentTree(self.base_array, min, 10*100)
        self._seg_max = SegmentTree(self.base_array, max, -10*100)
        self._lca_finder = LCAFinder(edges, root)

    def query_sum(self, u: int, v: int) -> int:
        """
        Returns the sum of values along the path between nodes `u` and `v`, inclusive.
        """
        if u not in self.nodes or v not in self.nodes:
            raise KeyError("One or both nodes not in the tree")
        lca = self._lca_finder.lowest_common_ancestor(u, v)
        node_u = self.nodes[u]
        node_v = self.nodes[v]
        node_lca = self.nodes[lca]
        res_u = self._query_up(node_u, node_lca, self._seg_sum)
        res_v = self._query_up(node_v, node_lca, self._seg_sum)
        return res_u + res_v - node_lca.value


    def query_min(self, u: int, v: int) -> int:
        """
        Returns the minimum value along the path between nodes `u` and `v`, inclusive.
        """
        if u not in self.nodes or v not in self.nodes:
            raise KeyError("One or both nodes not in the tree")
        lca = self._lca_finder.lowest_common_ancestor(u, v)
        node_u = self.nodes[u]
        node_v = self.nodes[v]
        node_lca = self.nodes[lca]
        res_u = self._query_up(node_u, node_lca, self._seg_min)
        res_v = self._query_up(node_v, node_lca, self._seg_min)
        return min(res_u, res_v)


    def query_max(self, u: int, v: int) -> int:
        """
        Returns the maximum value along the path between nodes `u` and `v`, inclusive.
        """
        if u not in self.nodes or v not in self.nodes:
            raise KeyError("One or both nodes not in the tree")
        lca = self._lca_finder.lowest_common_ancestor(u, v)
        node_u = self.nodes[u]
        node_v = self.nodes[v]
        node_lca = self.nodes[lca]
        res_u = self._query_up(node_u, node_lca, self._seg_max)
        res_v = self._query_up(node_v, node_lca, self._seg_max)
        return max(res_u, res_v)
    
    def query_lca(self, u: int, v: int) -> int:
        """
        Returns label of the lowest common ancestor of nodes `u` and `v`.
        
        Parameters:
            u (int): The first node.
            v (int): The second second.
        
        Returns:
            int: The label of the lowest common ancestor.
        
        Raises:
            KeyError: If either `u` or `v` do not exist in the tree.
        """
        if u not in self.nodes:
            raise KeyError(f"Given node {u} is not in the tree")
        if v not in self.nodes:
            raise KeyError(f"Given node {v} is not in the tree")
        return self._lca_finder.lowest_common_ancestor(u, v)
    
    def _query_up(self, node: HLD.Node, ancestor: HLD.Node, segtree: SegmentTree) -> int:
        """
        Queries the path from `node` up to `ancestor` (inclusive) using HLD decomposition.

        Parameters:
            node (HLD.Node): The starting node.
            ancestor (HLD.Node): The ancestor node to stop at.
            segtree (SegmentTree): The segment tree to query.

        Returns:
            int: The aggregated result along the path.
        """
        result = segtree.default
        while node.head is not ancestor.head:
            assert node.head is not None
            result = segtree.operation(result, segtree.query(node.head.pos, node.pos))
            assert node.head.parent is not None
            node = node.head.parent
        result = segtree.operation(result, segtree.query(ancestor.pos, node.pos))
        return result

    def _dfs(self, current_node: HLD.Node, parent: HLD.Node | None, depth: int) -> None:
        """
        Performs DFS on the tree to determine the heaviest child of each node.

        Parameters:
            current_node (HLD.Node): The current node in the recursive DFS.
            parent (HLD.Node | None): The previous node in the recursive DFS, or `None` if this node is the first.
            depth (int): The depth in the current recursion, starting at `0` at the root.
        """
        current_node.parent = parent
        current_node.depth = depth
        current_node.size = 1
        max_size = 0

        for neighboring_node in current_node.adjacent_nodes:
            if neighboring_node is not parent:
                self._dfs(neighboring_node, current_node, depth + 1)
                current_node.size += neighboring_node.size
                if neighboring_node.size > max_size:
                    max_size = neighboring_node.size
                    current_node.heavy = neighboring_node

    def _decompose(self, current_node: HLD.Node, head: HLD.Node) -> None:
        """
        Recursively plits a tree into heavy paths, favoring the heaviest child to keep the number of paths small.

        Paramters:
            current_node (HLD.Node): The current node in the recursive decomposition.
            head (HLD.Node): The head of the current path.
        """
        current_node.head = head
        current_node.pos = self.current_pos
        self.current_pos += 1

        if current_node.heavy is not None:
            self._decompose(current_node.heavy, head)

        for neighboring_node in current_node.adjacent_nodes:
            if neighboring_node is not current_node.parent and neighboring_node is not current_node.heavy:
                self._decompose(neighboring_node, neighboring_node)

    def _query_path(self, node_u: HLD.Node, node_v: HLD.Node, segtree: SegmentTree) -> int:
        """
        Queries the segment tree for `node_u` and `node_v`.

        Paramters:
            node_u (HLD.Node): The path's first endpoint.
            node_v (HLD.Node): The path's second endpoint.
            segtree (SegmentTree): The segment tree to query on.
        
        Returns:
            int: The result of the query.
        """
        result = segtree.default
        while node_u.head is not node_v.head:
            assert node_u.head is not None
            assert node_v.head is not None
            if node_u.head.depth < node_v.head.depth:
                node_u, node_v = node_v, node_u
            head_u = node_u.head
            assert head_u is not None
            result = segtree.operation(result, segtree.query(head_u.pos, node_u.pos))
            assert head_u.parent is not None
            node_u = head_u.parent
        if node_u.depth > node_v.depth:
            node_u, node_v = node_v, node_u
        result = segtree.operation(result, segtree.query(node_u.pos, node_v.pos))
        return result
