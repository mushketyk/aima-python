from aima.core.search.Framework import TreeSearch, Problem
from aima.core.search.Informed import AStarSearch
from aima.core.search.tests.Problem import TestHeuristicFunction, InformedTestActionFunction, InformedTestResultFunction, InformedTestGoalTest

__author__ = 'Ivan Mushketik'

import unittest

class AStarSearchTest(unittest.TestCase):
    def test_search_successful(self):
        ts = TreeSearch()
        ass = AStarSearch(ts, TestHeuristicFunction(9))

        p = Problem(1, InformedTestActionFunction(3), InformedTestResultFunction(), InformedTestGoalTest(9))

        result = ass.search(p)
        self.assertFalse(ass.is_failure(result))
        self.assertEqual(4, len(result))

    def test_search_failed(self):
        ts = TreeSearch()
        ass = AStarSearch(ts, TestHeuristicFunction(9))

        # This problem is unsolvable
        p = Problem(1, InformedTestActionFunction(3, 3), InformedTestResultFunction(), InformedTestGoalTest(9))

        result = ass.search(p)
        self.assertTrue(ass.is_failure(result))


if __name__ == '__main__':
    unittest.main()
