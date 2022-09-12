# Ahmed Ali (101181126)
# SYSC 2100 Winter 2022 Assignment 2

"""Class PriorityQueue implements the priority queue interface using a
min-heap as the underlying data structure.

Priorities are integers. The smaller the integer, the higher the
priority; for example, 0 is a higher priority than 10. The remove/delete_min
and find_min operations always return the item with the highest priority.
"""

# History:
# Version 1.00 Apr. 4, 2022 - Initial release.

import ctypes
from typing import Any

# A heap is a complete binary tree. Class PriorityQueue represents this tree
# as an array, laying out the nodes in breadth-first order.


def left(i: int) -> int:
    """Return the index of the left child of the node at index i in the array.
    """
    return 2 * i + 1


def right(i: int) -> int:
    """Return the index of the right child of the node at index i in the array.
    """
    return 2 * (i + 1)


def parent(i: int) -> int:
    """Return the index of the parent of the node at index i in the array."""
    return (i - 1) // 2


class PriorityQueue:
    def __init__(self, iterable=[]) -> None:
        """Initialize this PriorityQueue with the contents of iterable.

        If iterable isn't provided, the new priority queue is empty.

        >>> pq = PriorityQueue()
        >>> len(pq)
        0
        >>> pq = PriorityQueue([["purple", 5], ["black", 1], ["orange", 3],
                                ["white", 1], ["green", 0], ["yellow", 5]])
        >>> len(pq)
        6
        """
        self._a = _new_array(1)
        self._n = 0
        for item, priority in iterable:
            self.add(item, priority)  # add() updates self._n

    def __str__(self) -> str:
        """Return a string representation of this PriorityQueue."""
        if self._n is None:
            return '[]'
        return "[{0}]".format(", ".join(["({0})".format(", ".join([str(i) for i in self._a[x]])) for x in range(self._n)]))

    def __len__(self) -> int:
        """Return the number of items in this PriorityQueue."""
        return self._n

# Operations in the priority queue interface are:
# add, remove/delete_min and find_min.

    def add(self, item: Any, priority: int) -> bool:
        """Insert item in this PriorityQueue, assigning it the specified
        priority, and return True.

        >>> pq = PriorityQueue()
        >>> pq.add("purple", 5)
        >>> pq.add("black", 1)
        >>> pq.add("orange", 3)
        >>> pq.add("white", 1)
        >>> pq.add("green", 0)
        >>> pq.add("yellow", 5)

        >>> pq.find_min()
        "green"
        """
        # Here's the unmodified code from class BinaryHeap.

        # Double the capacity of the heap's array if it's full.
        if len(self._a) < self._n + 1:
            self._resize()

        self._a[self._n] = item, priority
        self._n += 1
        # "Bubble" x up the heap's tree until the heap property has been
        # restored.
        self._bubble_up(self._n - 1)
        return True

    def _bubble_up(self, i: int) -> None:
        """Bubble the most-recently added item (at index i in the heap's
        array) up the tree until it reaches the position where the heap
        property is restored.
        """
        # Here's the unmodified code from class BinaryHeap.

        # Repeatedly swap x with its parent, until x is no longer smaller
        # than its parent.
        p = parent(i)
        while i > 0 and self._a[i][1] < self._a[p][1]:
            self._a[i], self._a[p] = self._a[p], self._a[i]
            i = p
            p = parent(i)

    def remove(self) -> Any:
        """Remove and return the item with the highest priority in this
        PriorityQueue.

        Raise an IndexError if the queue is empty.

        >>> pq = PriorityQueue([["purple", 5], ["black", 1], ["orange", 3],
                                ["white", 1], ["green", 0], ["yellow", 5]])
        >>> pq.remove()
        "green"
        >>> len(pq)
        5

        >>> while len(pq) > 0:
        ...     pq.remove()
        ...
        >>> len(pq)
        0

        >>> pq.remove()
        builtins.IndexError: remove from an empty PriorityQueue
        """
        # Here's the unmodified code from class BinaryHeap.

        if self._n == 0:
            raise IndexError("remove: empty heap")

        x = self._a[0]  # Smallest value
        self._a[0] = self._a[self._n - 1]   # Replace the root element
        self._n -= 1

        # "Trickle" the root element down the heap's tree until the heap
        # property has been restored.
        self._trickle_down(0)

        # Decrease the capacity of the heap's array if less than 1/3 of it
        # is used.
        if 3 * self._n < len(self._a):
            self._resize()
        return x[0]

    # The highest priority value can be removed by calling delete_min
    # instead of remove.
    delete_min = remove

    def _trickle_down(self, i: int) -> None:
        """Trickle the item at index i in the heap's array down the tree
        until it reaches the position where the heap property has been restored.
        """
        # Here's the unmodified code from class BinaryHeap.

        # Repeatedly swap the element with its smallest child, until the
        # element is smaller than its children.
        while i >= 0:
            j = -1  # Index of the child node that will be swapped with its
            # parent.

            # Compare the node at index i with its right child, if it has one.
            r = right(i)
            if r < self._n and self._a[r][1] < self._a[i][1]:
                # The node at index i has two children, and is bigger than
                # its right child. Determine which child is the smallest.
                l = left(i)
                if self._a[l][1] < self._a[r][1]:
                    # The left child is the smallest child, so we'll swap
                    # the parent and its left child.
                    j = l
                else:
                    # The right child is the smallest child, so we'll swap
                    # the parent and its right child.
                    j = r
            else:
                # This chunk of code handles two cases:
                # Case 1: the node at index i doesn't have a right child,
                # so compare the node at index i with its left child,
                # if it has one.
                # Case 2: the node at index i has a right child, but it's
                # smaller than the right child, so compare the node at
                # index i with its left child.

                l = left(i)
                if l < self._n and self._a[l][1] < self._a[i][1]:
                    # The node at index i is bigger than its left child,
                    # so we'll swap the two nodes.
                    j = l

            if j >= 0:
                self._a[j], self._a[i] = self._a[i], self._a[j]

            i = j  # If a swap occurred, the element we're trickling down
            # is now at index i.

    def find_min(self) -> Any:
        """Return the item with the highest priority in this priority queue.

        >>> pq = PriorityQueue([["purple", 5], ["black", 1], ["orange", 3],
                                ["white", 1], ["green", 0], ["yellow", 5]])

        >>> pq.find_min()
        "green"

        >>> while len(pq) > 0:
        ...     pq.remove()
        ...
        >>> len(pq)
        0

        >>> pq.find_min()
        builtins.IndexError: find_min: empty PriorityQueue
        """
        # Here's the unmodified code from class BinaryHeap.

        if self._n == 0:
            raise IndexError("find_min: empty heap")
        return self._a[0][0]

    def _resize(self) -> None:
        """Change the capacity of this heap's array to 2 * n, where n is the
        number of elements in the heap. If the heap is empty, change the
        array's capacity to 1.
        """
        # Here's the unmodified code from class BinaryHeap.

        b = _new_array(max(2 * self._n, 1))
        b[0:self._n] = self._a[0:self._n]
#         for i in range(self._n):
#             b[i] = self._a[i]
        self._a = b

# Pat's new_array function uses numpy. We're using Python's ctypes module,
# so that students don't have to install numpy.


def _new_array(capacity: int) -> 'py_object_Array_<capacity>':
    """Return a new array with the specified capacity that stores
    references to Python objects.
    """
    # Here's the unmodified code from class BinaryHeap.

    if capacity <= 0:
        raise ValueError('new_array: capacity must be > 0')
    PyCArrayType = ctypes.py_object * capacity
    a = PyCArrayType()
    for i in range(len(a)):
        a[i] = None
    return a


if __name__ == '__main__':
    pq = PriorityQueue([["purple", 5], ["black", 1], ["orange", 3],
                        ["white", 1], ["green", 0], ["yellow", 5]])
    assert pq.find_min() == "green"
    print(pq)
    print(pq.find_min())
    print(pq.remove())
    print(pq.find_min())
    print(pq.remove())
    print(pq.find_min())
    print(pq.remove())
    print(pq.find_min())
    print(pq.remove())
    print(pq.find_min())
    print(pq.remove())
    print(pq.find_min())
    print(pq.remove())
    # print(pq.find_min())
    # print(pq.remove())
    assert len(pq) == 0
