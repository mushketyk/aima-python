from unittest import TestCase
from aima.core.agent import EnvironmentView, NoOpAction
from aima.core.environment.map import ExtendableMap, MapEnvironment, MapActionFunction, MapGoalTestFunction, MapStepCostFunction, MapPerceptToStateFunction, MoveToAction
from aima.core.search.online import OnlineDFSAgent, OnlineSearchProblem

__author__ = 'proger'

import unittest

# Mock class that listens to the actions of an online search agent and
# checks if it makes correct actions
class EnvironmentViewMock(EnvironmentView):
    def __init__(self, expected_actions):
        self.expected_actions = expected_actions
        self.pos = 0

    def agent_acted(self, agent, action, resulting_state):
        expected_action = self.expected_actions[self.pos]

        if expected_action  != action:
            raise RuntimeError("Expected: " + str(expected_action) + " but received " + str(action))

        self.pos += 1

# Convert list of locations into a list of MoveToAction objects
def _get_move_to_actions_array(locations):
    return [MoveToAction(location) for location in locations] + [NoOpAction()]


class OnlineDFSAgentTest(unittest.TestCase):
    def setUp(self):
        map = ExtendableMap()
        map.add_bidirectional_link("A", "B", 5)
        map.add_bidirectional_link("A", "C", 6)
        map.add_bidirectional_link("B", "D", 4)
        map.add_bidirectional_link("B", "E", 7)
        map.add_bidirectional_link("D", "F", 4)
        map.add_bidirectional_link("D", "G", 8)

        self.map = map

    def test_already_at_goal(self):
        me = MapEnvironment(self.map)
        agent = OnlineDFSAgent(OnlineSearchProblem(MapActionFunction(self.map), MapGoalTestFunction("A"), MapStepCostFunction(self.map)),
                               MapPerceptToStateFunction())

        me.add_new_agent(agent, "A")
        expected_actions = [NoOpAction()]
        me.add_environment_view(EnvironmentViewMock(expected_actions))
        
        me.step_until_done()

    def test_normal_search(self):
        me = MapEnvironment(self.map)
        agent = OnlineDFSAgent(OnlineSearchProblem(MapActionFunction(self.map), MapGoalTestFunction("G"), MapStepCostFunction(self.map)),
                               MapPerceptToStateFunction())

        me.add_new_agent(agent, "A")
        locations = ['C', 'A', 'B', 'A', 'B', 'E', 'B', 'D', 'B', 'D', 'G']
        expected_actions = _get_move_to_actions_array(locations)
        me.add_environment_view(EnvironmentViewMock(expected_actions))

        me.step_until_done()

    def test_no_path(self):
        map = ExtendableMap()
        map.add_bidirectional_link('A', 'B', 1)
        me = MapEnvironment(map)
        agent = OnlineDFSAgent(OnlineSearchProblem(MapActionFunction(map), MapGoalTestFunction("G"), MapStepCostFunction(map)),
                               MapPerceptToStateFunction())

        me.add_new_agent(agent, "A")
        locations = ['B', 'A', 'B', 'A']
        expected_actions = _get_move_to_actions_array(locations)
        me.add_environment_view(EnvironmentViewMock(expected_actions))

        me.step_until_done()

if __name__ == '__main__':
    unittest.main()
