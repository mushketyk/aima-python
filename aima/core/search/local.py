from math import exp
from random import randint, uniform
from aima.core import search
from aima.core.search import utils
from aima.core.search.framework import NodeExpander, Node
from aima.core.util.other import Infinity

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

 # Artificial Intelligence A Modern Approach (3rd Edition): Figure 4.2, page 122.
 #
 # function HILL-CLIMBING(problem) returns a state that is a local maximum
 #
 #   current <- MAKE-NODE(problem.INITIAL-STATE)
 #   loop do
 #     neighbor <- a highest-valued successor of current
 #     if neighbor.VALUE <= current.VALUE then return current.STATE
 #     current <- neighbor
 #
class HillClimbingSearch(NodeExpander):
    """
    The most basic algorithm of local search. At each state al reachable states from the current one are expanded. Current
    state is substituted by a state with the best heuristic estimation (if one exists). If all expanded states' heuristic
    estimation is worse that the current state's estimation, the search is over.
    """
    def __init__(self, heuristic_function):
        super().__init__()
        self.heuristic_function = heuristic_function

    def is_failure(self):
        return self.failure != False

    # function HILL-CLIMBING(problem) returns a state that is a local maximum
    def search(self, problem):
        self.clear_instrumentation()

        self.failure = True
        self.last_state = None
        # current <- MAKE-NODE(problem.INITIAL-STATE)
        current_node = Node(problem.get_initial_state())

        while True:
            children = self.expand_node(current_node, problem)
            # neighbor <- a highest-valued successor of current
            neighbor = self._get_lowest_valued_node(children)
            
            # if neighbor.VALUE <= current.VALUE then return current.STATE
            if neighbor == None or self._get_value(current_node) <= self._get_value(neighbor):
                if search.Utils.is_goal_state(problem, current_node):
                    self.failure = False
                self.last_state = current_node.get_state()
                return search.Utils.actions_from_nodes(current_node.get_path_from_root())

            # current <- neighbor
            current_node = neighbor

    def _get_lowest_valued_node(self, children):
        """
        Get node with the lowest (the best) estimation of heuristic function
        :param children: children of current node
        :return: node with the best heuristic estimation
        """
        lowest_value = Infinity()
        node_with_lowest_value = None

        for node in children:
            value = self._get_value(node)
            if value < lowest_value:
                node_with_lowest_value = node
                lowest_value = value

        return node_with_lowest_value

    def _get_value(self, node):
        return self.heuristic_function.h(node.get_state())


class Scheduler:
    def __init__(self, k=20, lam=0.045, limit=100):
        self.k = k
        self.lam = lam
        self.limit = limit

    def get_temp(self, time):
        if time < self.limit:
            return self.k * exp(-1 * self.lam * time)
        else:
            return 0

 # Artificial Intelligence A Modern Approach (3rd Edition): Figure 4.5, page 126.
 #
 # function SIMULATED-ANNEALING(problem, schedule) returns a solution state
 #
 #   current <- MAKE-NODE(problem.INITIAL-STATE)
 #   for t = 1 to INFINITY do
 #     T <- schedule(t)
 #     if T = 0 then return current
 #     next <- a randomly selected successor of current
 #     /\E <- next.VALUE - current.value
 #     if /\E > 0 then current <- next
 #     else current <- next only with probability e^(/\E/T)
 #
 # Figure 4.5 The simulated annealing search algorithm, a version of
 # stochastic hill climbing where some downhill moves are allowed. Downhill
 # moves are accepted readily early in the annealing schedule and then less
 # often as time goes on. The schedule input determines the value of
 # the temperature T as a function of time.
class SimulateAnnealingSearch(NodeExpander):
    def __init__(self, heuristic_function, scheduler=Scheduler()):
        super().__init__()
        self.heuristic_function = heuristic_function
        self.scheduler = scheduler

    def failed(self):
        return self.failure != False

    # function SIMULATED-ANNEALING(problem, schedule) returns a solution state
    def search(self, problem):
        self.clear_instrumentation()
        self.failure = True
        self.last_state = None
        # current <- MAKE-NODE(problem.INITIAL-STATE)
        current_node = Node(problem.get_initial_state())
        # for t = 1 to INFINITY do
        time_step = 0
        while True:
            # temperature <- schedule(t)
            temperature = self.scheduler.get_temp(time_step)
            time_step += 1
            # if temperature = 0 then return current
            if temperature == 0:
                if search.utils.is_goal_state(problem, current_node):
                    self.failure = False
                self.last_state = current_node.get_state()
                return search.utils.actions_from_nodes(current_node.get_path_from_root())

            children = self.expand_node(current_node, problem)

            number_of_children = len(children)
            if number_of_children != 0:
                # next <- a randomly selected successor of current
                next = children[randint(0, number_of_children - 1)]
                # /\E <- next.VALUE - current.value
                delta_e = self._get_value(current_node) - self._get_value(next)

                if self._should_accept(temperature, delta_e):
                    current_node = next

    def _probability_of_acceptance(self, temperature, delta_e):
        return exp(delta_e / temperature)

    # if /\E > 0 then current <- next
	# else current <- next only with probability e^(/\E/T)
    def _should_accept(self, temperature, delta_e):
        if delta_e > 0:
            return True
        else:
            return uniform(0, 1) <= self._probability_of_acceptance(temperature, delta_e)

    def _get_value(self, node):
        return self.heuristic_function.h(node.get_state())

