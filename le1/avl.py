class AVLTree:
    """
    An AVL tree is a self-balancing binary search tree implementation that checks
    the heights of its subtrees and rotates accordingly if imbalanced after every
    operation to ensure that the tree remains balanced.

    Given a treap with n nodes, here are its operations' time complexities:
        - contains: O(log n)
        - add: O(log n)
        - remove: O(log n)
    """
    def __init__(self) -> None:
        self._root: _AVLNode | None = None
        self._size = 0
    
    @property
    def size(self) -> int:
        """The number of values currently in the AVL tree."""
        return self.size

    def contains(self, value: int) -> bool:
        """
        Returns `True` if `value` exists in the AVL tree, and `False` otherwise. If the
        AVL tree is empty, `False` is returned automatically

        Parameters:
            value (int): The value to search for.
        
        Returns:
            bool: Whether the value exists in the treap.
        """
        return _AVLNode.search(self._root, value) is not None

    def add(self, value: int) -> bool:
        """
        Inserts a new value into the AVL tree if it doesn't exist.

        Parameters:
            value (int): The value to insert.
        
        Returns:
            bool: `True` if the value was successfully inserted, `False` if it already exists.
        """
        self._root, success = _AVLNode.insert(self._root, value)
        if success:
            self._size += 1
        return success
    
    def remove(self, value: int) -> bool:
        """
        Removes a value from the AVL tree if it exists.

        Parameters:
            value (int): The value to remove.
        
        Returns:
            bool: True if the value was successfully removed, False if it was not found.
        """
        self._root, success = _AVLNode.delete(self._root, value)
        if success:
            self._size -= 1
        return success


class _AVLNode:
    """
    Internal node class used by the AVLTree. Each node stores:
        - a value (int)
        - its height (int)
        - references to left and right child nodes

    The AVL tree maintains the binary search tree property (ordered by value)
    and ensures balance by checking subtree heights and performing rotations.
    """
    def __init__(self, value: int) -> None:
        self._value = value
        self._height = 0
        self._left: _AVLNode | None = None
        self._right: _AVLNode | None = None
    
    @property
    def value(self) -> int:
        """The value stored in this node."""
        return self.value
    
    @staticmethod
    def search(node: _AVLNode | None, value: int) -> _AVLNode | None:
        """
        Searches for a value in the AVL tree starting from the given node.

        Parameters:
            node (_AVLNode | None): The root of the subtree to search.
            value (int): The value to search for.
        
        Returns:
            _AVLNode|None: The node containing the value, or `None` if not found.
        """
        if node is None:
            return None
        elif value < node.value:
            return _AVLNode.search(node._left, value)
        elif value > node.value:
            return _AVLNode.search(node._right, value)
        else:
            return node
    
    @staticmethod
    def insert(node: _AVLNode | None, value: int) -> tuple[_AVLNode | None, bool]:
        """
        Inserts a new value into the AVL tree rooted at `node`.

        Parameters:
            node (_AVLNode | None): The root of the subtree.
            value (int): The value to insert.
        
        Returns:
            tuple[_AVLNode|None,bool]:
                - The new root of the subtree.
                - Whether insertion succeeded.
        """
        if node is None:
            return _AVLNode(value), True
        elif value < node.value:
            node._left, success = _AVLNode.insert(node._left, value)
        elif value > node.value:
            node._right, success = _AVLNode.insert(node._right, value)
        else:
            return node, False
        
        node = _AVLNode._rebalance(node)
        return node, success
    
    @staticmethod
    def delete(node: _AVLNode | None, value: int) -> tuple[_AVLNode | None, bool]:
        """
        Deletes a value from the AVL tree rooted at `node`.

        Parameters:
            node (_AVLNode | None): The root of the subtree.
            value (int): The value to delete.
        
        Returns:
            tuple[_AVLNode|None,bool]:
                - The new root of the subtree.
                - Whether insertion succeeded.
        """
        if node is None:
            return None, False
        elif value < node.value:
            node._left, success = _AVLNode.delete(node._left, value)
        elif value > node.value:
            node._right, success = _AVLNode.delete(node._right, value)
        else:
            success = True
            if node._left is None or node._right is None:
                return node._left or node._right, True
            else:
                successor = node._right
                while successor._left:
                    successor = successor._left
                node._value = successor.value
                node._right, _ = _AVLNode.delete(node._right, successor.value)
        
        node = _AVLNode._rebalance(node)
        return node, success
    
    @staticmethod
    def height(node: _AVLNode | None) -> int:
        """Returns the height of the given node, or -1 if `None` was given."""
        return node._height if node is not None else -1
    
    @staticmethod
    def _rebalance(node: _AVLNode) -> _AVLNode:
        """
        Rebalances the AVL tree rooted at `node` if it is imbalanced.

        Parameters:
            node (_AVLNode): The root of the subtree.
        
        Returns:
            _AVLNode: The new root of the subtree after rebalancing.
        """
        node._height = 1 + max(_AVLNode.height(node._left), _AVLNode.height(node._right))
        balance = _AVLNode.height(node._left) - _AVLNode.height(node._right)
        
        if balance > 1:
            assert node._left is not None
            if _AVLNode.height(node._left._left) >= _AVLNode.height(node._left._right):
                node = _AVLNode._rotate_right(node)
            else:
                node._left = _AVLNode._rotate_left(node._left)
                node = _AVLNode._rotate_right(node)
        elif balance < -1:
            assert node._right is not None
            if _AVLNode.height(node._right._right) >= _AVLNode.height(node._right._left):
                node = _AVLNode._rotate_left(node)
            else:
                node._right = _AVLNode._rotate_right(node._right)
                node = _AVLNode._rotate_left(node)
        
        return node
    
    @staticmethod
    def _rotate_left(node: _AVLNode) -> _AVLNode:
        """
        Performs a left rotation on the given node.

        Parameters:
            node (_AVLNode): The root of the subtree to rotate.
        
        Returns:
            _AVLNode: The new root after rotation.
        """
        assert node._right is not None
        new_root = node._right
        node._right = new_root._left
        new_root._left = node
        
        node._height = 1 + max(_AVLNode.height(node._left), _AVLNode.height(node._right))
        new_root._height = 1 + max(_AVLNode.height(new_root._left), _AVLNode.height(new_root._right))
        
        return new_root
    
    @staticmethod
    def _rotate_right(node: _AVLNode) -> _AVLNode:
        """
        Performs a right rotation on the given node.

        Parameters:
            node (_AVLNode): The root of the subtree to rotate.
        
        Returns:
            _AVLNode: The new root after rotation.
        """
        assert node._left is not None
        new_root = node._left
        node._left = new_root._right
        new_root._right = node
        
        node._height = 1 + max(_AVLNode.height(node._left), _AVLNode.height(node._right))
        new_root._height = 1 + max(_AVLNode.height(new_root._left), _AVLNode.height(new_root._right))
        
        return new_root