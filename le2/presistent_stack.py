from typing import Generic, TypeVar


T = TypeVar("T")


class PersistentStack(Generic[T]):
    """
    A persistent stack implementation, where each push or pop returns a new
    stack,leaving the old one unchanged while maintaining `O(1)` operations.
    """
    class Node:
        def __init__(self, value: T) -> None:
            self._value = value
            self.previous: PersistentStack.Node | None = None
        
        @property
        def value(self) -> T:
            return self._value

    def __init__(self, head: PersistentStack.Node | None=None):
        self._head = head
    
    def push(self, v: T) -> PersistentStack[T]:
        """
        Return a new stack with `v` pushed on top.

        Parameters:
            v (T): The value to push.

        Returns:
            PersistentStack[T]: A new persistent stack with `v` at the top.
        """
        new_node = PersistentStack.Node(v)
        new_node.previous = self._head
        return PersistentStack(new_node)
    
    def pop(self) -> PersistentStack[T]:
        """
        Return a new stack with the top element removed.

        Returns:
            PersistentStack[T]: A new persistent stack without the top element.

        Raises:
            IndexError: If the stack is empty.
        """
        if self._head is None:
            raise IndexError("Stack is empty.")
        return PersistentStack(self._head.previous)
    
    def top(self) -> T:
        """
        Return the value at the top of the stack.

        Returns:
            T: The value stored at the top.

        Raises:
            IndexError: If the stack is empty.
        """
        if self._head is None:
            raise IndexError("Stack is empty.")
        return self._head.value
    
    def empty(self) -> bool:
        """
        Check if the stack is empty.

        Returns:
            bool: `True` if the stack has no elements, `False` otherwise.
        """
        return self._head is None


class StackHistory(Generic[T]):
    """
    Maintains a history of versions of a PersistentStack, allowing efficient undo/redo operations.

    Each push or pop creates a new version of the stack, which is appended to the history.
    """
    def __init__(self) -> None:
        self._versions: list[PersistentStack[T]] = [PersistentStack()]
        self._current_version: int = 0

    def current(self) -> "PersistentStack[T]":
        """
        Return the current version of the stack.

        Returns:
            PersistentStack[T]: The most recent active stack version.
        """
        return self._versions[self._current_version]

    def push(self, v: T) -> None:
        """
        Push a value onto the current stack, creating a new version.

        Parameters:
            v (T): The value to push.
        """
        new_version = self.current().push(v)
        if self._versions[-1] is self.current():
            self._versions.append(new_version)
        else:
            self._versions[self._current_version + 1] = new_version
        self._current_version += 1

    def pop(self) -> None:
        """
        Pop the top value from the current stack, creating a new version.

        Raises:
            IndexError: If the current stack is empty.
        """
        new_version = self.current().pop()
        if self._versions[-1] is self.current():
            self._versions.append(new_version)
        else:
            self._versions[self._current_version + 1] = new_version
        self._current_version += 1

    def undo(self, k: int) -> None:
        """
        Undo the last `k` operations (pushes or pops). If `k` is greater than
        the number of operations so far, then the persistent stack is reverted
        to the initial state (empty).

        Parameters:
            k (int): The number of operations to undo.
        """
        self._current_version -= min(k, self._current_version)