class UnionFind:
    """
    Union Find is a data structure that can perform unite and
    same-set checking in practically constant time.
    """
    def __init__(self):
        self._nodes: dict[int, _UnionFindNode] = {}
    
    def _get_root(self, node: _UnionFindNode) -> _UnionFindNode:
        """
        Obtains the root of the given node, compressing the path along
        the way. Note that the parent of a node is initially itself.

        Params:
            node (_UnionFindNode): The given node
        
        Returns:
            _UnionFindNode: The given node's root
        """
        if node.parent is not node:
            node.parent = self._get_root(node.parent) 
        return node.parent
    
    def unite(self, i: int, j: int) -> bool:
        """
        Unites the set containing `node i` and the set containing `node j`.
        Implements unison by rank to keep other operations fast.
        Returns `True` if the unison was successful, or `False` otherwise
        (i.e. they are already united beforehand).

        Params:
            i (int): Label of node i
            j (int): Label of node j
        
        Returns:
            bool: Whether the unison was successful
        """
        if i in self._nodes:
            node_i = self._nodes[i]
        else:
            node_i = _UnionFindNode(i)
            self._nodes[i] = node_i

        if j in self._nodes:
            node_j = self._nodes[j]
        else:
            node_j = _UnionFindNode(j)
            self._nodes[j] = node_j

        root_i = self._get_root(node_i)
        root_j = self._get_root(node_j)

        if root_i == root_j:
            return False

        # Union by Rank: Put root of lower rank under root of higher rank
        # to minimize total tree height. If roots have the same rank,
        # arbitrarily choose one to be the new root and increment that
        # root's rank.
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
        Returns `True` if `node i` and `node j` are connected,and `False`
        otherwise. If at least one of the two nodes do not exist, then
        `False` is returned automatically.

        Params:
            i (int): Label of node i
            j (int): Label of node j
        
        Returns:
            bool: Whether node i and node j are in the same set
        """
        if i not in self._nodes or j not in self._nodes:
            return False

        return self._get_root(self._nodes[i]) == self._get_root(self._nodes[j])

    
class _UnionFindNode:
    """
    This implementation of Union Find will use nodes instead of
    the usual hard array implementation. Each node has an integer
    label (to be given to the constructor), a parent node (initially
    itself), and a rank (initially 0).
    """
    def __init__(self, label: int):
        self._label = label
        self.parent = self
        self.rank = 0

    @property
    def label(self) -> int:
        return self._label