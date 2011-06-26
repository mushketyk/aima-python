from aima.core.AgentImpl import NoOpAction
from aima.core.environment.Map import RomaniaCities, get_simplified_road_map_of_part_of_romania, MapResultFunction, MapGoalTestFunction, MapActionFunction, MapHeuristicFunction, MapStepCostFunction
from aima.core.search.Framework import TreeSearch, Problem, HeuristicFunction, ResultFunction
from aima.core.search.Informed import AStarSearch, RecursiveBestFirstSearch, AStarEvaluationFunction
from aima.core.search.tests.Problem import TestHeuristicFunction, InformedTestActionFunction, InformedTestResultFunction, InformedTestGoalTest
from aima.core.util.Datastructure import Point2D

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


class RecursiveBestFirstSearchTest(unittest.TestCase):
    # Test that use figure from AIMA second edition
    def test_aima2_figure_4_4(self):
        finish = RomaniaCities.BUCHAREST
        start = RomaniaCities.ARAD
        rm = get_simplified_road_map_of_part_of_romania()
        rbfs = RecursiveBestFirstSearch(AStarEvaluationFunction(MapHeuristicFunction(rm, finish)))

        p = Problem(start, MapActionFunction(rm), MapResultFunction(), MapGoalTestFunction(finish), MapStepCostFunction(rm))

        result = rbfs.search(p)
        self.assertFalse(rbfs.is_failure(result))
        self.assertEquals(4, len(result))

        self.assertEqual(RomaniaCities.SIBIU, result[0].location)
        self.assertEqual(RomaniaCities.RIMNICU_VILCEA, result[1].location)
        self.assertEqual(RomaniaCities.PITESTI, result[2].location)
        self.assertEqual(RomaniaCities.BUCHAREST, result[3].location)

    def test_search_start_at_goal_state(self):
        finish = RomaniaCities.BUCHAREST
        start = RomaniaCities.BUCHAREST
        rm = get_simplified_road_map_of_part_of_romania()
        rbfs = RecursiveBestFirstSearch(AStarEvaluationFunction(MapHeuristicFunction(rm, finish)))

        p = Problem(start, MapActionFunction(rm), MapResultFunction(), MapGoalTestFunction(finish), MapStepCostFunction(rm))

        result = rbfs.search(p)
        self.assertFalse(rbfs.is_failure(result))
        self.assertEqual(1, len(result))
        self.assertEqual(NoOpAction(), result[0])

if __name__ == '__main__':
    unittest.main()
