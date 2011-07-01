from aima.core.agent import NoOpAction
from aima.core.environment.map import RomaniaCities, get_simplified_road_map_of_part_of_romania, MapHeuristicFunction, MapStepCostFunction, MapActionFunction, MapResultFunction, MapGoalTestFunction
from aima.core.search.framework import TreeSearch, Problem
from aima.core.search.informed import AStarSearch, RecursiveBestFirstSearch, AStarEvaluationFunction

__author__ = 'Ivan Mushketik'

import unittest

class AStarSearchTest(unittest.TestCase):
    def test_aima2_figure_4_2(self):
        finish = RomaniaCities.BUCHAREST
        start = RomaniaCities.ARAD
        rm = get_simplified_road_map_of_part_of_romania()

        ts = TreeSearch()
        ass = AStarSearch(ts, MapHeuristicFunction(rm, finish))

        p = Problem(start, MapActionFunction(rm), MapResultFunction(), MapGoalTestFunction(finish), MapStepCostFunction(rm))

        result = ass.search(p)
        self.assertFalse(ass.is_failure(result))
        self.assertEquals(4, len(result))

        self.assertEqual(RomaniaCities.SIBIU, result[0].location)
        self.assertEqual(RomaniaCities.RIMNICU_VILCEA, result[1].location)
        self.assertEqual(RomaniaCities.PITESTI, result[2].location)
        self.assertEqual(RomaniaCities.BUCHAREST, result[3].location)

    def test_search_start_at_goal_state(self):
        finish = RomaniaCities.BUCHAREST
        start = RomaniaCities.BUCHAREST
        rm = get_simplified_road_map_of_part_of_romania()

        ts = TreeSearch()
        ass = AStarSearch(ts, MapHeuristicFunction(rm, finish))

        p = Problem(start, MapActionFunction(rm), MapResultFunction(), MapGoalTestFunction(finish), MapStepCostFunction(rm))

        result = ass.search(p)
        self.assertFalse(ass.is_failure(result))
        self.assertEqual(1, len(result))
        self.assertEqual(NoOpAction(), result[0])


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
