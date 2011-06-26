from aima.core.Agent import Action
from aima.core.search.Framework import ActionFunction, ResultFunction, GoalTest, Problem, HeuristicFunction

__author__ = 'Ivan Mushketik'

# Simplem problem for testing
# Every state is a number. Action function generate 3 stub actions if state number is less then a specified limit
#

class TestAction(Action):
    def __init__(self):
        super().__init__("testAction")

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


# Simple problem for informed search.
# Each state is a number and each action is a number in (1, n). Result function adds action number of a state to create
# new state. Goal of a problem to reach some number x in the least number of steps.

class InformedTestAction(Action):
    def __init__(self, number):
        self.number = number

    def is_noop(self):
        return False

class InformedTestActionFunction(ActionFunction):
    def __init__(self, limit, search_limit = None):
        self._limit = limit
        self._search_limit = search_limit

    def actions(self, state):

        if self._search_limit and state > self._search_limit:
            return []

        return [InformedTestAction(n) for n in range(1, self._limit)]

class InformedTestResultFunction(ResultFunction):
    def result(self, state, action):
        return state + action.number

class InformedTestGoalTest(GoalTest):
    def __init__(self, goal):
        self.goal = goal

    def is_goal_state(self, state):
        return state == self.goal

class TestHeuristicFunction(HeuristicFunction):
    def __init__(self, goal):
        self._goal = goal

    def h(self, state):
        return self._goal - state