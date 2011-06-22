from abc import ABCMeta
from heapq import heappush, heappop

__author__ = 'Ivan Mushketik'

class Queue(metaclass=ABCMeta):
    """
        Base class for queue implementation
    """
    def __init__(self):
        self._list = []

    def is_empty(self):
        """
            Check if queue is empty

            return True if equeue is empty, or False otherwise
        """
        return len(self._list) == 0

    def add(self, element):
        """
            Add new element to a queue.

            element - new element to add
        """
        raise NotImplementedError

    def element(self):
        """
            Return first element from a queue

            return first element if queue isn't empty, or None otherwise
        """
        if self.is_empty():
            return None
        else:
            return self._list[0]

    def pop(self):
        """
            Remove first element from a queue

            return return removed element if queue was not empty, or None otherwise
        """
        raise NotImplementedError

    def length(self):
        """ Return number of elements in a queue """
        return len(self._list)


class LIFOQueue(Queue):
    def __init__(self):
        super().__init__()

    def add(self, element):
        self._list.insert(0, element)

    def pop(self):
        if self.is_empty():
            return None
        else:
            return self._list.pop(0)
        

class FIFOQueue(Queue):
    def __init__(self):
        super().__init__()

    def add(self, element):
        self._list.append(element)

    def pop(self):
        if self.is_empty():
            return None
        else:
            return self._list.pop(0)


class PriorityQueue(Queue):
    def __init__(self):
        super().__init__()

    def add(self, element):
        heappush(self._list, element)

    def pop(self):
        if self.is_empty():
            return None
        else:
            return heappop(self._list)