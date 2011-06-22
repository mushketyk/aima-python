from aima.core.util.Datastructure import LIFOQueue, FIFOQueue, PriorityQueue

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

    def test_remove_add(self):
        lifo = LIFOQueue()

        lifo.add(1)
        lifo.add(2)
        lifo.add(3)

        self.assertEqual(3, lifo.length())
        self.assertEqual(3, lifo.pop())
        self.assertEqual(2, lifo.pop())
        self.assertEqual(1, lifo.pop())


class TestFIFOQueue(unittest.TestCase):
    def test_is_empty(self):
        fifo = FIFOQueue()
        self.assertTrue(fifo.is_empty(), "New queue should be empty")

        fifo.add(1)
        self.assertFalse(fifo.is_empty(), "Queue with added element shouldn't be empty")

        fifo.pop()
        self.assertTrue(fifo.is_empty(), "When all elements removed from a queue it should be empty")

    def test_remove_add(self):
        fifo = FIFOQueue()

        fifo.add(1)
        fifo.add(2)
        fifo.add(3)

        self.assertEqual(3, fifo.length())
        self.assertEqual(1, fifo.pop())
        self.assertEqual(2, fifo.pop())
        self.assertEqual(3, fifo.pop())

        
class TestPriorityQueue(unittest.TestCase):
    def test_is_empty(self):
        priorityQueue = PriorityQueue()
        self.assertTrue(priorityQueue.is_empty(), "New queue should be empty")

        priorityQueue.add(1)
        self.assertFalse(priorityQueue.is_empty(), "Queue with added element shouldn't be empty")

        priorityQueue.pop()
        self.assertTrue(priorityQueue.is_empty(), "When all elements removed from a queue it should be empty")

    def test_remove_add(self):
        priorityQueue = PriorityQueue()

        priorityQueue.add(5)
        priorityQueue.add(10)
        priorityQueue.add(1)
        priorityQueue.add(11)

        self.assertEqual(4, priorityQueue.length())
        self.assertEqual(1, priorityQueue.pop())
        self.assertEqual(5, priorityQueue.pop())
        self.assertEqual(10, priorityQueue.pop())
        self.assertEqual(11, priorityQueue.pop())

if __name__ == '__main__':
    unittest.main()
