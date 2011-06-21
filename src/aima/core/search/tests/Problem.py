from aima.core.Agent import Action
from aima.core.search.Framework import ActionFunction, ResultFunction, GoalTest, Problem

__author__ = 'Ivan Mushketik'

# Simplem problem for testing
# Every state is a number. Action function generate 3 stub actions if state number is less then a specified limit
#

class TestAction(Action):
    def is_noop(self):
        return False

class TestActionsFunction(ActionFunction):
    """
        Limit is specified to test failure and cutoffs in searches
    """
    def __init__(self, limit=None):
        self.limit = limit

    def actions(self, state):
        res = []

        if not self.limit or self.limit > state:
            for i in range(0, 3):
                res.append(TestAction())

        return res

class TestResultFunction(ResultFunction):
    def result(self, state, action):
        return state + 1

class TestGoalTest(GoalTest):
    def __init__(self, goal):
        self.goal = goal

    def is_goal_state(self, state):
        return state == self.goal

