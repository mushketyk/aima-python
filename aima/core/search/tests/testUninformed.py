from aima.core.search.Framework import Problem, TreeSearch, GraphSearch
from aima.core.search.Uninformed import DepthLimitedSearch, IterativeDeepeningSearch, DepthFirstSearch, BreadthFirstSearch
from aima.core.search.tests.Problem import TestActionsFunction, TestResultFunction, TestGoalTest

__author__ = 'Ivan Mushketik'

import unittest

class TestBreathFirstSearch(unittest.TestCase):
    def test_successful_search(self):
        ts = TreeSearch()
        bfs = BreadthFirstSearch(ts)
        problem = Problem(1, TestActionsFunction(), TestResultFunction(), TestGoalTest(5))

        result = bfs.search(problem)
        self.assertEqual(4, len(result))
        
        metrics = bfs.get_metrics();
        self.assertEqual(14, metrics[ts.METRIC_NODES_EXPANDED])
        self.assertEqual(4, metrics[ts.METRIC_PATH_COST])

    def test_failed_search(self):
        ts = TreeSearch()
        bfs = BreadthFirstSearch(ts)
        problem = Problem(1, TestActionsFunction(3), TestResultFunction(), TestGoalTest(5))

        result = bfs.search(problem)
        self.assertTrue(bfs.is_failure(result))

    def test_successful_search_with_graph_search(self):
        gs = GraphSearch()
        bfs = BreadthFirstSearch(gs)
        problem = Problem(1, TestActionsFunction(), TestResultFunction(), TestGoalTest(5))

        result = bfs.search(problem)
        self.assertEqual(4, len(result))

        metrics = bfs.get_metrics();
        self.assertEqual(4, metrics[gs.METRIC_NODES_EXPANDED])
        self.assertEqual(4, metrics[gs.METRIC_PATH_COST])


class TestDepthFirstSearch(unittest.TestCase):
    def test_successful_search(self):
        ts = TreeSearch()
        dfs = DepthFirstSearch(ts)
        problem = Problem(1, TestActionsFunction(), TestResultFunction(), TestGoalTest(4))

        result = dfs.search(problem)
        self.assertEqual(3, len(result))
        metrics = dfs.get_metrics();
        self.assertEqual(3, metrics[ts.METRIC_NODES_EXPANDED])
        self.assertEqual(3, metrics[ts.METRIC_PATH_COST])

    def test_search_failure(self):
        ts = TreeSearch()
        dfs = DepthFirstSearch(ts)
        # 5 - is a goal state but it's unreachable
        problem = Problem(1, TestActionsFunction(3), TestResultFunction(), TestGoalTest(5))

        result = dfs.search(problem)
        self.assertTrue(dfs.is_failure(result))
        metrics = dfs.get_metrics();
        self.assertEqual(13, metrics[ts.METRIC_NODES_EXPANDED])

class TestDepthLimitSearch(unittest.TestCase):
    def test_successful_search(self):
        dls = DepthLimitedSearch(10)
        problem = Problem(1, TestActionsFunction(), TestResultFunction(), TestGoalTest(4))

        result = dls.search(problem)
        self.assertEquals(3, len(result))

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

class TestIterativeDeepeningSearch(unittest.TestCase):
    
    def test_successful_search(self):
        ids = IterativeDeepeningSearch()
        problem = Problem(1, TestActionsFunction(), TestResultFunction(), TestGoalTest(4))

        result = ids.search(problem)
        self.assertEquals(3, len(result))

    def test_search_failure(self):
        ids = IterativeDeepeningSearch()
        # 5 - is a goal state but it's unreachable
        problem = Problem(1, TestActionsFunction(2), TestResultFunction(), TestGoalTest(5))

        result = ids.search(problem)
        self.assertTrue(ids.is_failure(result))

if __name__ == '__main__':
    unittest.main()
