from abc import ABCMeta
from math import sqrt

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
        if self.is_empty():
            return None
        else:
            return self._list.pop(0)

    def length(self):
        """ Return number of elements in a queue """
        return len(self._list)

    def remove(self, to_remove):
        """
            Remove element from a queue

            to_remove - element to remove
            return - if element was deleted return true. Returns false otherwise.
        """
        if to_remove in self._list:
            self._list.remove(to_remove)
            return True
        else:
            return False
        

class LIFOQueue(Queue):
    def __init__(self):
        super().__init__()

    def add(self, element):
        self._list.insert(0, element)


class FIFOQueue(Queue):
    def __init__(self):
        super().__init__()

    def add(self, element):
        self._list.append(element)

class PriorityQueue(Queue):
    def __init__(self, comparator):
        super().__init__()
        self._comparator = comparator

    def add(self, element):
        (pos, found) = self._binary_search(element)
        self._list.insert(pos, element)

    def remove(self, element):
        (pos, found) = self._binary_search(element)
        if found:
            del self._list[pos]
        return found

    def _binary_search(self, element):
        l = 0
        r = len(self._list) - 1

        while l <= r:
            m = (l + r) // 2
            middle_el = self._list[m]

            if self._comparator.compare(middle_el, element) < 0:
                l = m + 1
            elif self._comparator.compare(middle_el, element) > 0:
                r = m - 1
            else:
                return (m, True)

        return (l, False)


class Point2D:
    """
        Point to two-dimensional space
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def distance(self, point):
        x_diff = self.x - point.x
        y_diff = self.y - point.y

        return sqrt(x_diff * x_diff + y_diff * y_diff)


class LabeledGraph:
    """
        Directed labeled graph. Each vertex and each edge between vertexes has a label
    """
    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex):
        """
            Add a vertex to a graph. If a vertex already exist in graph no vertex will be added.
        """
        if self.graph.get(vertex) == None:
            self.graph[vertex] = {}

    def remove_vertex(self, vertex):
        """
            Remove vertex from a graph
        """
        if self.graph.get(vertex) != None:
            del self.graph[vertex]

    def set_edge(self, from_vertex, to_vertex, label):
        """
            Set label for an edge between from_vertex and to_vertex. If no edge exists between this vertexes
            new edge will be created
        """
        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)
        self.graph[from_vertex][to_vertex] = label

    def get_edge(self, from_vertex, to_vertex):
        """
            Get label from edge. If no edge exists None is returned
        """
        if self.graph.get(from_vertex) != None and self.graph.get(to_vertex) != None:
            return self.graph[from_vertex][to_vertex]
        else:
            return None

    def remove_edge(self, from_vertex, to_vertex):
        """
            Remove edge from a graph if one exists
        """
        self.set_edge(from_vertex, to_vertex, None)

    def vertexes(self):
        """
            Get all vertexes in a graph
        """
        return self.graph.keys()

    def get_successors(self, vertex):
        """
            Get vertexes connected to a specified vertex
        """
        if self.graph.get(vertex) != None:
            return self.graph[vertex].keys()
        else:
            return None

