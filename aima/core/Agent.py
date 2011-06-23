from abc import ABCMeta

__author__ = 'Ivan Mushketik'

class Action(metaclass=ABCMeta):

    def is_noop(self):
        raise NotImplementedError()


class EnvironmentObject(metaclass=ABCMeta):
    pass

class EnvironmentState(metaclass=ABCMeta):
    pass

class Model(metaclass=ABCMeta):
    pass

class Percept(metaclass=ABCMeta):
    pass

class State(metaclass=ABCMeta):
    pass