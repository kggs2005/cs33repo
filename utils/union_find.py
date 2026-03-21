class UnionFind:
    """
    Disjoint Set Union (Union-Find) data structure with path compression and union by rank.

    This structure efficiently supports operations to determine whether two elements
    are in the same set and to unite two sets.
    """
    class Node:
        """
        Represents a node in the Union-Find structure.

        Parameters:
            label (int): The integer label identifying the node.
        """
        def __init__(self, label: int):
            self._label = label
            self.parent = self
            self.rank = 0

        @property
        def label(self) -> int:
            """The label of the node."""
            return self._label

    def __init__(self):
        self._nodes: dict[int, UnionFind.Node] = {}
    
    def unite(self, i: int, j: int) -> bool:
        """
        Unites the sets containing elements `i` and `j`.

        Parameters:
            i (int): The label of the first element.
            j (int): The label of the second element.

        Returns:
            bool: `True` if the sets were successfully united, `False` if they were already in the same set.
        """
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
        """
        Determines whether elements `i` and `j` belong to the same set.

        Parameters:
            i (int): The label of the first element.
            j (int): The label of the second element.

        Returns:
            bool: `True` if both elements are in the same set, `False` otherwise.
            If either of the elements do not exist, then `False` is returned automatically.
        """
        if i not in self._nodes or j not in self._nodes:
            return False
        return self._get_root(self._nodes[i]) == self._get_root(self._nodes[j])
    
    def _get_root(self, node: UnionFind.Node) -> UnionFind.Node:
        """
        Finds the root of the set containing the given node, compressing the path along the way.

        Parameters:
            node (UnionFind.Node): The node whose set root is to be found.

        Returns:
            UnionFind.Node: The root node of the set containing the given node.
        """
        if node.parent is not node:
            node.parent = self._get_root(node.parent) 
        return node.parent