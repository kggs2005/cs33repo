from random import random


class Treap:
    """
    A treap is a self-balancing binary search tree implementation that assigns
    each node a random priority and uses the functionlity of a heap ("treap" = 
    "tree" + "heap") to ensure that the tree remains balanced.

    Given a treap with n nodes, here are its operations' time complexities:
        - contains: O(log n)
        - add: O(log n)
        - remove: O(log n)
    """
    def __init__(self) -> None:
        self._root: _TreapNode | None = None
        self._size = 0
    
    @property
    def size(self) -> int:
        """The number of values currently in the treap."""
        return self._size

    def contains(self, value: int) -> bool:
        """
        Returns `True` if `value` exists in the treap, and `False` otherwise. If the
        treap is empty, `False` is returned automatically

        Args:
            value (int): The value to search for.
        
        Returns:
            bool: Whether the value exists in the treap.
        """
        return _TreapNode.search(self._root, value) is not None

    def add(self, value: int) -> bool:
        """
        Inserts a new value into the treap if it doesn't exist.

        Args:
            value (int): The value to insert.
        
        Returns:
            bool: `True` if the value was successfully inserted, `False` if it already exists.
        """
        self._root, success = _TreapNode.insert(self._root, value)
        if success:
            self._size += 1
        return success
    
    def remove(self, value: int) -> bool:
        """
        Removes a value from the treap if it exists.

        Args:
            value (int): The value to remove.
        
        Returns:
            bool: True if the value was successfully removed, False if it was not found.
        """
        self._root, success = _TreapNode.delete(self._root, value)
        if success:
            self._size -= 1
        return success


class _TreapNode:
    """
    Internal node class used by the Treap. Each node stores:
        - a value (int)
        - a randomly assigned priority (float between 0 and 1)
        - references to left and right child nodes

    The treap maintains both the binary search tree property (ordered by value)
    and the heap property (ordered by priority).
    """
    def __init__(self, value: int) -> None:
        self._value = value
        self._priority = random()
        self._left: _TreapNode | None = None
        self._right: _TreapNode | None = None
    
    @property
    def value(self) -> int:
        """The value stored in this node."""
        return self._value
    
    @staticmethod
    def search(node: _TreapNode | None, value: int) -> _TreapNode | None:
        """
        Searches for a value in the treap starting from the given node.

        Args:
            node (_TreapNode | None): The root of the subtree to search.
            value (int): The value to search for.
        
        Returns:
            _TreapNode|None: The node containing the value, or `None` if not found.
        """
        if node is None:
            return None
        elif value < node.value:
            return _TreapNode.search(node._left, value)
        elif value > node.value:
            return _TreapNode.search(node._right, value)
        else:
            return node
    
    @staticmethod
    def insert(node: _TreapNode | None, value: int) -> tuple[_TreapNode | None, bool]:
        """
        Inserts a new value into the treap rooted at `node`.

        Args:
            node (_TreapNode | None): The root of the subtree.
            value (int): The value to insert.
        
        Returns:
            tuple[_TreapNode|None,bool]:
                - The new root of the subtree.
                - Whether insertion succeeded.
        """
        if _TreapNode.search(node, value) is not None:
            return node, False
        
        left, middle, right = _TreapNode._split(node, value)
        assert middle is None
        new_node = _TreapNode(value)
        return _TreapNode._merge(_TreapNode._merge(left, new_node), right), True
    
    @staticmethod
    def delete(node: _TreapNode | None, value: int) -> tuple[_TreapNode | None, bool]:
        """
        Deletes a value from the treap rooted at `node`.

        Args:
            node (_TreapNode | None): The root of the subtree.
            value (int): The value to delete.
        
        Returns:
            tuple[_TreapNode|None,bool]:
                - The new root of the subtree.
                - Whether insertion succeeded.
        """
        if _TreapNode.search(node, value) is None:
            return node, False
        
        left, middle, right = _TreapNode._split(node, value)
        assert middle is not None
        return _TreapNode._merge(left, right), True
    
    @staticmethod
    def _split(node: _TreapNode | None, value: int) -> tuple[_TreapNode | None, _TreapNode | None, _TreapNode | None]:
        """
        Splits the treap rooted at `node` into three parts:
            - left: nodes with values less than `value`
            - middle: node with value equal to `value` (or `None` if not found)
            - right: nodes with values greater than `value`

        Args:
            node (_TreapNode | None): The root of the subtree.
            value (int): The value to split around.
        
        Returns:
            tuple[_TreapNode|None,_TreapNode|None,_TreapNode|None]: (left, middle, right) subtrees.
        """
        if node is None:
            return None, None, None
        elif value < node.value:
            left, middle, right = _TreapNode._split(node._left, value)
            node._left = right
            return left, middle, node
        elif value > node.value:
            left, middle, right = _TreapNode._split(node._right, value)
            node._right = left
            return node, middle, right
        else:
            left, right = node._left, node._right
            node._left = node._right = None
            return left, node, right
    
    @staticmethod
    def _merge(left: _TreapNode | None, right: _TreapNode | None) -> _TreapNode | None:
        """
        Merges two treaps into one while maintaining both the BST and heap properties.

        Args:
            left (_TreapNode | None): Root of the left treap.
            right (_TreapNode | None): Root of the right treap.
        
        Returns:
            _TreapNode|None: The root of the merged treap.
        """
        if left is None or right is None:
            return left or right
        elif left._priority > right._priority:
            left._right = _TreapNode._merge(left._right, right)
            return left
        else:
            right._left = _TreapNode._merge(left, right._left)
            return right