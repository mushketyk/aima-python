from aima.core.util.datastructure import LIFOQueue, FIFOQueue, PriorityQueue, LabeledGraph
from aima.core.util.other import Comparator


__author__ = 'Ivan Mushketik'

import unittest



class TestLIFOQueue(unittest.TestCase):
    def test_is_empty(self):
        lifo = LIFOQueue()
        self.assertTrue(lifo.is_empty(), "New queue should be empty")

        lifo.add(1)
        self.assertFalse(lifo.is_empty(), "Queue with added element shouldn't be empty")

        lifo.pop()
        self.assertTrue(lifo.is_empty(), "When all elements removed from a queue it should be empty")

    def test_pop_add(self):
        lifo = LIFOQueue()

        lifo.add(1)
        lifo.add(2)
        lifo.add(3)

        self.assertEqual(3, lifo.length())
        self.assertEqual(3, lifo.pop())
        self.assertEqual(2, lifo.pop())
        self.assertEqual(1, lifo.pop())

    def test_remove(self):
        lifo = LIFOQueue()

        lifo.add(1)
        lifo.add(2)
        lifo.add(3)

        self.assertFalse(lifo.remove(5))
        self.assertTrue(lifo.remove(2))

        self.assertEqual(2, lifo.length())
        self.assertEqual(3, lifo.pop())
        self.assertEqual(1, lifo.pop())

class TestFIFOQueue(unittest.TestCase):
    def test_is_empty(self):
        fifo = FIFOQueue()
        self.assertTrue(fifo.is_empty(), "New queue should be empty")

        fifo.add(1)
        self.assertFalse(fifo.is_empty(), "Queue with added element shouldn't be empty")

        fifo.pop()
        self.assertTrue(fifo.is_empty(), "When all elements removed from a queue it should be empty")

    def test_pop_add(self):
        fifo = FIFOQueue()

        fifo.add(1)
        fifo.add(2)
        fifo.add(3)

        self.assertEqual(3, fifo.length())
        self.assertEqual(1, fifo.pop())
        self.assertEqual(2, fifo.pop())
        self.assertEqual(3, fifo.pop())

    def test_remove(self):
        fifo = FIFOQueue()

        fifo.add(1)
        fifo.add(2)
        fifo.add(3)

        self.assertFalse(fifo.remove(5))
        self.assertTrue(fifo.remove(2))

        self.assertEqual(2, fifo.length())
        self.assertEqual(1, fifo.pop())
        self.assertEqual(3, fifo.pop())
        
class TestPriorityQueue(unittest.TestCase):
    class TestComparator(Comparator):
        def compare(self, first, second):
            return second - first


    def test_is_empty(self):
        priorityQueue = PriorityQueue(TestPriorityQueue.TestComparator())
        self.assertTrue(priorityQueue.is_empty(), "New queue should be empty")

        priorityQueue.add(1)
        self.assertFalse(priorityQueue.is_empty(), "Queue with added element shouldn't be empty")

        priorityQueue.pop()
        self.assertTrue(priorityQueue.is_empty(), "When all elements removed from a queue it should be empty")

    def test_pop_add(self):
        priorityQueue = PriorityQueue(TestPriorityQueue.TestComparator())

        priorityQueue.add(5)
        priorityQueue.add(10)
        priorityQueue.add(1)
        priorityQueue.add(11)
        priorityQueue.add(3)

        self.assertEqual(5, priorityQueue.length())

        self.assertEqual(11, priorityQueue.pop())
        self.assertEqual(10, priorityQueue.pop())
        self.assertEqual(5, priorityQueue.pop())
        self.assertEqual(3, priorityQueue.pop())
        self.assertEqual(1, priorityQueue.pop())


    def test_remove_in_the_middle(self):
        priorityQueue = PriorityQueue(TestPriorityQueue.TestComparator())

        priorityQueue.add(5)
        priorityQueue.add(10)
        priorityQueue.add(1)
        priorityQueue.add(11)

        self.assertFalse(priorityQueue.remove(50))
        self.assertTrue(priorityQueue.remove(10))

        self.assertEqual(3, priorityQueue.length())
        self.assertEqual(11, priorityQueue.pop())
        self.assertEqual(5, priorityQueue.pop())
        self.assertEqual(1, priorityQueue.pop())

    def test_remove_at_the_beginning(self):
        priorityQueue = PriorityQueue(TestPriorityQueue.TestComparator())

        priorityQueue.add(5)
        priorityQueue.add(10)
        priorityQueue.add(1)
        priorityQueue.add(11)

        self.assertTrue(priorityQueue.remove(11))

        self.assertEqual(3, priorityQueue.length())
        self.assertEqual(10, priorityQueue.pop())
        self.assertEqual(5, priorityQueue.pop())
        self.assertEqual(1, priorityQueue.pop())

    def test_remove_at_the_end(self):
        priorityQueue = PriorityQueue(TestPriorityQueue.TestComparator())

        priorityQueue.add(5)
        priorityQueue.add(10)
        priorityQueue.add(1)
        priorityQueue.add(11)

        self.assertTrue(priorityQueue.remove(1))

        self.assertEqual(3, priorityQueue.length())
        self.assertEqual(11, priorityQueue.pop())
        self.assertEqual(10, priorityQueue.pop())
        self.assertEqual(5, priorityQueue.pop())


class LabeledGraphTest(unittest.TestCase):
    def test_get_vertexes(self):
        lg = LabeledGraph()
        expected_vertexes = ('vertex1', 'vertex2')

        for vertex in expected_vertexes:
            lg.add_vertex(vertex)

        result_vertexes = lg.vertexes()
        self.assertEqual(2, len(result_vertexes))
        self.assertEqual(set(expected_vertexes), set(result_vertexes))

    def test_set_label(self):
        lg = LabeledGraph()
        lg.set_edge('v1', 'v2', 5)
        lg.set_edge('v2', 'v3', 10)

        self.assertEqual(5, lg.get_edge('v1', 'v2'))
        self.assertEqual(10, lg.get_edge('v2', 'v3'))

    def test_remove_vertex(self):
        lg = LabeledGraph()
        lg.set_edge('t1', 's1', 2)
        lg.set_edge('t1', 's2', 3)

        lg.remove_vertex('t1')

        exp_vertexes = ['s1', 's2']
        self.assertEqual(set(lg.vertexes()), set(exp_vertexes))

        self.assertEqual(None, lg.get_edge('t1', 's1'))
        self.assertEqual(None, lg.get_edge('t1', 's2'))

    def test_get_successors(self):
        lg = LabeledGraph()
        lg.set_edge('s1', 't1', 10)
        lg.set_edge('s1', 't2', 10)
        lg.set_edge('s1', 't3', 10)

        lg.set_edge('s2', 't1', 10)
        lg.set_edge('s2', 't2', 10)

        self.assertEqual(set(lg.get_successors('s1')), set(['t1', 't2', 't3']))
        self.assertEqual(set(lg.get_successors('s2')), set(['t1', 't2']))

if __name__ == '__main__':
    unittest.main()
