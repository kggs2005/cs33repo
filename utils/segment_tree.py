from collections.abc import Callable


class SegmentTree:
    class Node:
        def __init__(self, left_index: int, right_index: int, value: int, default: int, operation: Callable[[int, int], int]) -> None:
            """
            Represents a node in the segment tree.

            Parameters:
                left_index (int): Left index of the segment.
                right_index (int): Right index of the segment.
                value (int): The aggregated value for this segment.
                default (int): The default value for empty segments.
                operation (Callable[[int,int],int]): The aggregation operation (sum, min, max).
            """
            self._left_index = left_index
            self._right_index = right_index
            self.value = value
            self._default = default
            self._operation = operation
            self.left_child: SegmentTree.Node | None = None
            self.right_child: SegmentTree.Node | None = None

        @property
        def left_index(self) -> int:
            return self._left_index
        
        @property
        def right_index(self) -> int:
            return self._right_index
        
        @property
        def default(self) -> int:
            return self._default
        
        @property
        def operation(self) -> Callable[[int, int], int]:
            return self._operation

    def __init__(self, data: list[int], operation: Callable[[int, int], int], default: int) -> None:
        """
        Builds a segment tree over the given data.

        Parameters:
            data (list[int]): The array of values.
            operation (Callable[[int,int],int]): The aggregation operation (sum, min, max).
            default (int): The default value for empty segments.
        """
        self.operation = operation
        self.default = default
        self.root = self._build(0, len(data) - 1, data)

    def _build(self, left_index: int, right_index: int, data: list[int]) -> SegmentTree.Node:
        if left_index == right_index:
            return SegmentTree.Node(left_index, right_index, data[left_index], self.default, self.operation)
        middle_index = (left_index + right_index) // 2
        left_child = self._build(left_index, middle_index, data)
        right_child = self._build(middle_index + 1, right_index, data)
        node = SegmentTree.Node(left_index, right_index, self.operation(left_child.value, right_child.value), self.default, self.operation)
        node.left_child = left_child
        node.right_child = right_child
        return node

    def query(self, left_index: int, right_index: int) -> int:
        """
        Queries the aggregated value in the range `[left_index, right_index]`.

        Parameters:
            left_index (int): Left index of the query range.
            right_index (int): Right index of the query range.

        Returns:
            int: The aggregated result over the range.
        """
        return self._query(self.root, left_index, right_index)

    def _query(self, node: SegmentTree.Node, left_index: int, right_index: int) -> int:
        if node.right_index < left_index or node.left_index > right_index:
            return self.default
        if left_index <= node.left_index and node.right_index <= right_index:
            return node.value
        left_value = self._query(node.left_child, left_index, right_index) if node.left_child else self.default
        right_value = self._query(node.right_child, left_index, right_index) if node.right_child else self.default
        return self.operation(left_value, right_value)

    def update(self, index: int, new_value: int) -> None:
        """
        Updates the value at a specific index.

        Parameters:
            index (int): The position to update.
            new_value (int): The new value to set.
        """
        self._update(self.root, index, new_value)

    def _update(self, node: SegmentTree.Node, index: int, new_value: int) -> None:
        assert node.left_index <= index <= node.right_index
        if node.left_index == node.right_index == index:
            node.value = new_value
            return
        elif node.left_child and index <= node.left_child.right_index:
            self._update(node.left_child, index, new_value)
        elif node.right_child:
            self._update(node.right_child, index, new_value)
        left_value = node.left_child.value if node.left_child else self.default
        right_value = node.right_child.value if node.right_child else self.default
        node.value = self.operation(left_value, right_value)