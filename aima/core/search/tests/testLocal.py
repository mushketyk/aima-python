from aima.core.search.Framework import Problem, ActionFunction, ResultFunction, GoalTest, HeuristicFunction
from aima.core.search.Local import HillClimbingSearch

__author__ = 'proger'

import unittest

#
# Simple problem for local search. State space is an array of numbers. State is a position in this array. Goal is
# to find position with the biggest number in array. Possible actions: move either left or rights (if possible).
# Heuristic function calculate, difference between the highest value in array and value in a current pos.
#


class LocalActionFunction(ActionFunction):
    def __init__(self, length):
        self.length = length

    def actions(self, state):
        if self.length == 0:
            return []
        elif state == 0:
            return [+1]
        elif state == (self.length - 1):
            return [-1]
        else:
            return [-1, +1]

class LocalResultFunction(ResultFunction):
    def result(self, state, action):
        return state + action

class LocalGoalTestFunction(GoalTest):
    def __init__(self, pos):
        self.pos = pos

    def is_goal_state(self, state):
        return state == self.pos

class LocalHeuristicFunction(HeuristicFunction):
    def __init__(self, values):
        self.max = max(values)
        self.values = values

    def h(self, state):
        return self.max - self.values[state]


    
class TestHillClimbingSearch(unittest.TestCase):
    def test_search_succeed(self):
        values = [4, 3, 5, 6, 10, 3]
        problem = Problem(1, LocalActionFunction(len(values)), LocalResultFunction(), LocalGoalTestFunction(4))
        hcs = HillClimbingSearch(LocalHeuristicFunction(values))
        actions = hcs.search(problem)
        
        self.assertFalse(hcs.is_failure())
        self.assertEqual(4, hcs.last_state)

    def test_search_failed(self):
        values = [4, 3, 5, 6, 3, 20, 3]

        problem = Problem(1, LocalActionFunction(len(values)), LocalResultFunction(), LocalGoalTestFunction(6))
        hcs = HillClimbingSearch(LocalHeuristicFunction(values))
        actions = hcs.search(problem)

        self.assertTrue(hcs.is_failure())
        self.assertEqual(3, hcs.last_state)

if __name__ == '__main__':
    unittest.main()
