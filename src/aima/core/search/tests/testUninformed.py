from aima.core.search.Framework import Problem
from aima.core.search.Uninformed import DepthLimitedSearch
from aima.core.search.tests.Problem import TestActionsFunction, TestResultFunction, TestGoalTest

__author__ = 'Ivan Mushketik'

import unittest

class TestDepthLimitSearch(unittest.TestCase):
    def test_successful_search(self):
        dls = DepthLimitedSearch(10)
        problem = Problem(1, TestActionsFunction(), TestResultFunction(), TestGoalTest(4))

        result = dls.search(problem)
        self.assertEquals(4, len(result))
        
        self.assertEquals(1, result[0].get_state())
        self.assertEquals(2, result[1].get_state())
        self.assertEquals(3, result[2].get_state())
        self.assertEquals(4, result[3].get_state())

    def test_search_cutoff(self):
        # Here we set depth limit 3...
        dls = DepthLimitedSearch(3)
        # But result can be found only with limit 4 or more
        problem = Problem(1, TestActionsFunction(), TestResultFunction(), TestGoalTest(5))

        result = dls.search(problem)
        self.assertTrue(dls.is_cutoff(result))
        self.assertFalse(dls.is_failure(result))


    def test_search_failure(self):
        dls = DepthLimitedSearch(10)
        # 5 - is a goal state but it's unreachable
        problem = Problem(1, TestActionsFunction(2), TestResultFunction(), TestGoalTest(5))

        result = dls.search(problem)
        self.assertFalse(dls.is_cutoff(result))
        self.assertTrue(dls.is_failure(result))


if __name__ == '__main__':
    unittest.main()
