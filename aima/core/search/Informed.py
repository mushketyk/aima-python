from aima.core.search.Framework import EvaluationFunction, PathCostFunction, PrioritySearch
from aima.core.util.Other import Comparator

__author__ = 'Ivan Mushketik'

# Artificial Intelligence A Modern Approach (3rd Edition): page 92.
class BestFirstSearch(PrioritySearch):
    """
        Base class for searches that fist explores node with a best path cost approximation
    """
    def __init__(self, queue_search, evaluation_function):
        super().__init__(queue_search)
        self._evaluation_function = evaluation_function

    def _get_comparator(self):
        ef = self._evaluation_function

        class BFSComparator(Comparator):
            def compare(self, node1, node2):
                f1 = ef.f(node1)
                f2 = ef.f(node2)

                return f1 - f2

        comparator = BFSComparator()
        return comparator


# Artificial Intelligence A Modern Approach (3rd Edition): page 93.
class AStarEvaluationFunction(EvaluationFunction):
    """
        Function that evaluate path cost from initial state to a goal state if path from root node to the current node
        is used.
    """
    def __init__(self, heuristic_function):
        self._heuristic_function = heuristic_function
        self._path_cost_function = PathCostFunction()

    def f(self, node):
        """
            f(n) = g(n) + h(n)
            Where:
            f(n) - result of this function
            g(n) - cost of a path from initial state to a current state
            h(n) - approximation of a path cost from a current state to a goal state
        """
        return self._path_cost_function.g(node) + self._heuristic_function.h(node.get_state())


# Artificial Intelligence A Modern Approach (3rd Edition): page 93.
class AStarSearch(BestFirstSearch):
    """
        This search explores nodes with the lowest evaluation of a search path cost. Search path cost is evaluated
        as a sum of path cost to an explored node and heuristic function result which is an approximation of a path cost
        from current state to a goal state.
    """
    def __init__(self, queue_search, heuristic_function):
        super().__init__(queue_search, AStarEvaluationFunction(heuristic_function))