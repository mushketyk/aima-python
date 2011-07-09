from aima.core.search.adversarial import MinMaxSearch, SuccessorFunction

__author__ = 'proger'

import unittest

class TestSuccessorFunction(SuccessorFunction):
    def __init__(self):
        successors = {}
        successors['A'] = [('B', 'a1', 1), ('C', 'a2', 1), ('D', 'a3', 1)]
        successors['B'] = [('E', 'b1', 1), ('F', 'b2', 1), ('G', 'b3', 1)]
        successors['C'] = [('H', 'c1', 1), ('I', 'c2', 1), ('J', 'c3', 1)]
        successors['D'] = [('K', 'd1', 1), ('L', 'd2', 1), ('M', 'd3', 1)]

        self.successors = successors

    def get_successor_states(self, state):
        return self.successors[state]

class TestUtilityFunction():
    def __init__(self):
        utility = {}
        utility['E'] = 3
        utility['F'] = 12
        utility['G'] = 8

        utility['H'] = 2
        utility['I'] = 4
        utility['J'] = 6

        utility['K'] = 14
        utility['L'] = 5
        utility['M'] = 2

        self.utility = utility

    def __call__(self, state):
        return self.utility[state]

class TestTerminalFunction():
    def __init__(self):
        self.terminal_states = {'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'}

    def __call__(self, state):
        return state in self.terminal_states

class MinMaxSearchTest(unittest.TestCase):
    def test_get_action(self):
        mms = MinMaxSearch(TestSuccessorFunction(), TestUtilityFunction(), TestTerminalFunction())
        action = mms.get_action('A')

        self.assertEquals('a1', action)

if __name__ == '__main__':
    unittest.main()
