from abc import ABCMeta

__author__ = 'Ivan Mushketik'

class Queue(metaclass=ABCMeta):
    def isEmpty(self):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def add(self, element):
        raise NotImplementedError

    def element(self):
        raise NotImplementedError

    def poll(self):
        raise NotImplementedError

    def peek(self):
        raise NotImplementedError

# TODO: Implement queues

class LIFOQueue(Queue):
    pass

class FIFOQueue(Queue):
    pass

class PriorityQueue(Queue):
    pass