from aima.core.search import Utils
from aima.core.search.Framework import EvaluationFunction, PathCostFunction, PrioritySearch, NodeExpander, Search, Node
from aima.core.search.Utils import actions_from_nodes
from aima.core.util.Other import Comparator, Infinity

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


# Artificial Intelligence A Modern Approach (3rd Edition): page 92.
class GreedyBestFirstSearchEvaluationFunction(EvaluationFunction):
    def __init__(self, heuristic_function):
        self._heuristic_function = heuristic_function

    def f(self, node):
        return self._heuristic_function.f(node)


# Artificial Intelligence A Modern Approach (3rd Edition): page 92.
class GreedyBestFirstSearch(BestFirstSearch):
    """
        BGFS explores nodes with better heuristic function evaluation first.
    """
    def __init__(self, queue_search, heuristic_function):
        super().__init__(queue_search, GreedyBestFirstSearchEvaluationFunction())
        

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

class SearchResult:
    def __init__(self, node, f_cost_limit):
        self._node = node
        self._f_cost_limit = f_cost_limit

    def found_solution(self):
        return self._node != None

    def get_solution(self):
        return self._node

    def get_f_cost_limit(self):
        return self._f_cost_limit

class RecursiveBestFirstSearch(NodeExpander, Search):
    MAX_RECURSIVE_DEPTH = "maxRecursiveDepth"
    PATH_COST = "pathCost"

    def __init__(self, evaluation_function):
        super().__init__()
        self._evaluation_function = evaluation_function

    def clear_instrumentation(self):
        super().clear_instrumentation()
        self._metrics[self.MAX_RECURSIVE_DEPTH] = 0
        self._metrics[self.PATH_COST] = 0

    def search(self, problem):
        self.clear_instrumentation()

        root_node = Node(problem.get_initial_state())
        sr = self._rbfs(problem, root_node, self._evaluation_function.f(root_node), Infinity(), 0)

        if sr.found_solution():
            goal_node = sr.get_solution()
            return Utils.actions_from_nodes(goal_node.get_path_from_root())
        else:
            return self._failure()

    def _rbfs(self, problem, node, node_f, f_limit, recursive_depth):
        self._set_max_recursive_depth(recursive_depth)

        if Utils.is_goal_state(problem, node):
            return SearchResult(node, f_limit)

        successors = self.expand_node(node ,problem)

        if len(successors) == 0:
            return SearchResult(None, Infinity())

        f = [min(self._evaluation_function.f(node), node_f) for node in successors]

        while True:
            best_index = self._get_best_f_value_index(f)
            if f[best_index] > f_limit:
                return SearchResult(None, f[best_index])

            alt_index = self._get_next_best_f_value_index(f, best_index)

            sr = self._rbfs(problem, successors[best_index], f[best_index], min(f_limit, f[alt_index]), recursive_depth + 1)

            if sr.found_solution():
                return sr

            f[best_index] = sr.get_f_cost_limit()

    def _get_best_f_value_index(self, f):
        best_index = 0
        for i in range(1, len(f)):
            if f[i] < f[best_index]:
                best_index = i

        return best_index

    def _get_next_best_f_value_index(self, f, best_index):
        alt_best_index = 0
        for i in range(1, len(f)):
            if f[i] < f[alt_best_index] and alt_best_index != best_index:
                alt_best_index = i

        return alt_best_index

    def get_path_cost(self):
        return self._metrics[self.PATH_COST]

    def _set_path_cost(self, path_cost):
        self._metrics[self.PATH_COST] = path_cost

    def get_max_recursive_depth(self):
        return self._metrics[self.MAX_RECURSIVE_DEPTH]

    def _set_max_recursive_depth(self, recursive_depth):
        max_recursive_depth = self._metrics[self.MAX_RECURSIVE_DEPTH]
        if recursive_depth > max_recursive_depth:
            self._metrics[self.MAX_RECURSIVE_DEPTH] = recursive_depth



