import math
from math import sin, cos
from aima.core.Agent import Action
from aima.core.search.Framework import StepCostFunction, HeuristicFunction, ResultFunction, GoalTest, ActionFunction
from aima.core.util.Datastructure import LabeledGraph, Point2D

__author__ = 'Ivan Mushketik'

class GeographicalMap:
    """
        Map to save information about locations, their coordinates and lengths of paths between them.
    """
    def __init__(self):
        self.clear()

    def clear(self):
        self.links = LabeledGraph()
        self.location_positions = {}

    def add_location(self, location):
        self.links.add_vertex(location)

    def get_locations(self):
        return self.links.vertexes()

    def is_location(self, location):
        return location in self.links.vertexes()

    def get_locations_linked_to(self, location):
        return self.links.get_successors(location)

    def get_distance(self, from_location, to_location):
        return self.links.get_edge(from_location, to_location)

    def add_unidirectional_link(self, from_location, to_location, distance):
        self.links.set_edge(from_location, to_location, distance)

    def add_bidirectional_link(self, from_location, to_location, distance):
        self.links.set_edge(from_location, to_location, distance)
        self.links.set_edge(to_location, from_location, distance)

    def remove_unidirectional_link(self, from_location, to_location):
        self.links.remove_edge(from_location, to_location)

    def remove_bidirectional_link(self, from_location, to_location):
        self.links.remove_edge(from_location, to_location)
        self.links.remove_edge(to_location, from_location)

    def set_position(self, location, pos):
        self.location_positions[location] = pos

    def get_position(self, location):
        return self.location_positions[location]

    def set_dist_and_dir_to_ref_location(self, location, dist, dir):
        coordinates = Point2D(-sin(dir * math.pi / 180) * dist, cos(dir * math.pi / 180) * dist)
        self.links.add_vertex(location)
        self.location_positions[location] = coordinates

class MapStepCostFunction(StepCostFunction):
    constant_cost = 1

    def __init__(self, map):
        self.map = map

    def c(self, state, action, newState):
        from_location = str(state)
        to_location = str(newState)

        distance = self.map.get_distance(from_location, to_location)

        if distance == None or distance <= 0:
            return self.constant_cost

        return distance


class MoveToAction(Action):
    def __init__(self, location):
        super().__init__("moveTo")
        self.location = location


class MapHeuristicFunction(HeuristicFunction):
    def __init__(self, map, goal):
        self.map = map
        self.goal = goal

    def h(self, state):
        pt1 = self.map.get_position(state)
        pt2 = self.map.get_position(self.goal)

        return pt1.distance(pt2)


class MapResultFunction(ResultFunction):
    def result(self, state, action):
        return action.location


class MapGoalTestFunction(GoalTest):
    def __init__(self, goal):
        self.goal = goal

    def is_goal_state(self, state):
        return state == self.goal

class MapActionFunction(ActionFunction):
    def __init__(self, map):
        self.map = map

    def actions(self, state):
        return [MoveToAction(location) for location in self.map.get_locations_linked_to(state)]


# AIMA ed. 2 uses simplified map of Romania as an example of informed and uninformed searches
class RomaniaCities:
    ORADEA = "Oradea"
    ZERIND = "Zerind"
    ARAD = "Arad"
    TIMISOARA = "Timisoara"
    LUGOJ = "Lugoj"
    MEHADIA = "Mehadia"
    DOBRETA = "Dobreta"
    SIBIU = "Sibiu"
    RIMNICU_VILCEA = "RimnicuVilcea"
    CRAIOVA = "Craiova"
    FAGARAS = "Fagaras"
    PITESTI = "Pitesti"
    GIURGIU = "Giurgiu"
    BUCHAREST = "Bucharest"
    NEAMT = "Neamt"
    URZICENI = "Urziceni"
    IASI = "Iasi"
    VASLUI = "Vaslui"
    HIRSOVA = "Hirsova"
    EFORIE = "Eforie"

def get_simplified_road_map_of_part_of_romania():
    """
        Get simplefied map of part of romania from AIMA 2 ed.
    """
    map = GeographicalMap()
    
    map.add_bidirectional_link(RomaniaCities.ORADEA, RomaniaCities.ZERIND, 71.0)
    map.add_bidirectional_link(RomaniaCities.ORADEA, RomaniaCities.SIBIU, 151.0)
    map.add_bidirectional_link(RomaniaCities.ZERIND, RomaniaCities.ARAD, 75.0)
    map.add_bidirectional_link(RomaniaCities.ARAD, RomaniaCities.TIMISOARA, 118.0)
    map.add_bidirectional_link(RomaniaCities.ARAD, RomaniaCities.SIBIU, 140.0)
    map.add_bidirectional_link(RomaniaCities.TIMISOARA, RomaniaCities.LUGOJ, 111.0)
    map.add_bidirectional_link(RomaniaCities.LUGOJ, RomaniaCities.MEHADIA, 70.0)
    map.add_bidirectional_link(RomaniaCities.MEHADIA, RomaniaCities.DOBRETA, 75.0)
    map.add_bidirectional_link(RomaniaCities.DOBRETA, RomaniaCities.CRAIOVA, 120.0)
    map.add_bidirectional_link(RomaniaCities.SIBIU, RomaniaCities.FAGARAS, 99.0)
    map.add_bidirectional_link(RomaniaCities.SIBIU, RomaniaCities.RIMNICU_VILCEA, 80.0)
    map.add_bidirectional_link(RomaniaCities.RIMNICU_VILCEA, RomaniaCities.PITESTI, 97.0)
    map.add_bidirectional_link(RomaniaCities.RIMNICU_VILCEA, RomaniaCities.CRAIOVA, 146.0)
    map.add_bidirectional_link(RomaniaCities.CRAIOVA, RomaniaCities.PITESTI, 138.0)
    map.add_bidirectional_link(RomaniaCities.FAGARAS, RomaniaCities.BUCHAREST, 211.0)
    map.add_bidirectional_link(RomaniaCities.PITESTI, RomaniaCities.BUCHAREST, 101.0)
    map.add_bidirectional_link(RomaniaCities.GIURGIU, RomaniaCities.BUCHAREST, 90.0)
    map.add_bidirectional_link(RomaniaCities.BUCHAREST, RomaniaCities.URZICENI, 85.0)
    map.add_bidirectional_link(RomaniaCities.NEAMT, RomaniaCities.IASI, 87.0)
    map.add_bidirectional_link(RomaniaCities.URZICENI, RomaniaCities.VASLUI, 142.0)
    map.add_bidirectional_link(RomaniaCities.URZICENI, RomaniaCities.HIRSOVA, 98.0)
    map.add_bidirectional_link(RomaniaCities.IASI, RomaniaCities.VASLUI, 92.0)
    # add_bidirectional_link(VASLUI - already all linked
    map.add_bidirectional_link(RomaniaCities.HIRSOVA, RomaniaCities.EFORIE, 86.0)
    # add_bidirectional_link(EFORIE - already all linked

    # distances and directions
    # reference location: Bucharest
    map.set_dist_and_dir_to_ref_location(RomaniaCities.ARAD, 366, 117)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.BUCHAREST, 0, 360)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.CRAIOVA, 160, 74)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.DOBRETA, 242, 82)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.EFORIE, 161, 282)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.FAGARAS, 176, 142)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.GIURGIU, 77, 25)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.HIRSOVA, 151, 260)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.IASI, 226, 202)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.LUGOJ, 244, 102)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.MEHADIA, 241, 92)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.NEAMT, 234, 181)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.ORADEA, 380, 131)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.PITESTI, 100, 116)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.RIMNICU_VILCEA, 193, 115)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.SIBIU, 253, 123)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.TIMISOARA, 329, 105)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.URZICENI, 80, 247)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.VASLUI, 199, 222)
    map.set_dist_and_dir_to_ref_location(RomaniaCities.ZERIND, 374, 125)

    return map