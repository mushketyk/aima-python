from abc import ABCMeta
from math import exp
from random import randint, uniform
import random
from urllib.request import randombytes
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
                if search.utils.is_goal_state(problem, current_node):
                    self.failure = False
                self.last_state = current_node.get_state()
                return search.utils.actions_from_nodes(current_node.get_path_from_root())

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

class StateConverter(metaclass=ABCMeta):
    def get_string(self, state):
        raise NotImplementedError()

    def get_state(self, string):
        raise NotImplementedError()

    def get_individual_length(self):
        raise NotImplementedError()

    def get_alphabet(self):
        raise NotImplementedError()

class GeneticProblem:
    def __init__(self, initial_states, goal_test, converter):
        self.initial_states = initial_states
        self.goal_test = goal_test
        self.converter = converter

    def is_goal_state(self, state):
        return self.goal_test.is_goal_state(state)

class GeneticAlgorithm:
    POPULATION_SIZE = "populationSize"
    NUMBER_OF_ITERATIONS = "numberOfIterations"

    def __init__(self, mutation_probability):
        self.mutation_probability = mutation_probability
        self.metrics = {}
        self.population = set()
        self.clear_instrumentation()

    def search(self, genetic_problem, heuristic_function, max_iterations):
        converter = genetic_problem.converter
        self.population = [converter.get_string(state) for state in genetic_problem.initial_states]

        self._validate_population(self.population, converter)
        self.clear_instrumentation()
        self._set_population_size(len(self.population))

        best_state = None

        for i in range(max_iterations):
            best_state = self._genetic_algorithm(genetic_problem, heuristic_function)

            self._set_iterations(i)
            if self._is_goal(genetic_problem, best_state):
                self.failed = False
                break

        return best_state

    def _genetic_algorithm(self, genetic_problem, heuristic_function):
        new_population = set()

        for i in range(len(self.population)):
            x = self._random_selection(self.population)
            y = self._random_selection(self.population)
            child = self._reproduce(x, y, genetic_problem)

            if self._to_mutate():
                child = self._mutate(child, genetic_problem)

            new_population.add(child)

        self.population = new_population

        return self._get_best_individual_state(genetic_problem.converter, heuristic_function)

    def _random_selection(self, population):
        population_list = list(population)

        return population_list[randint(0, len(population_list) - 1)]

    def _reproduce(self, x, y, problem):
        pos = randint(0, problem.converter.get_individual_length() - 1)

        return x[:pos] + y[pos:]

    def _to_mutate(self):
        prob = random.random()

        return prob < self.mutation_probability

    def _mutate(self, child, problem):
        alphabet = problem.converter.get_alphabet();
        ri = randint(0, len(child) - 1)
        r_char = alphabet[randint(0, len(alphabet) - 1)]

        return child[:ri] + r_char + child[ri + 1:]


    def _get_best_individual_state(self, converter, heuristic_function):
        states = [converter.get_state(individual) for individual in self.population]

        m = Infinity()
        best_state = None

        for state in states:
            hv = heuristic_function.h(state)
            if hv  < m:
                m = hv
                best_state = state

        return best_state

    def clear_instrumentation(self):
        self._set_iterations(0)
        self._set_population_size(0)
        self.failed = True

    def _validate_population(self, population, converter):
        if len(population) < 1:
            raise ValueError("Number of individuals in populations should be >= 1")

        expected_length = converter.get_individual_length()
        for individual in population:
            if len(individual) != expected_length:
                raise ValueError("Found individual '" + str(individual) + "' but only individuals with length "
                                 + str(expected_length) + " accepted")

    def _set_population_size(self, num):
        self.metrics[self.POPULATION_SIZE] = num

    def _set_iterations(self, num):
        self.metrics[self.NUMBER_OF_ITERATIONS] = num

    def _is_goal(self, problem, best_state):
        return problem.is_goal_state(best_state)
















