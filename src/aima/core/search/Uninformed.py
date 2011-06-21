
from aima.core.Agent import Action
from aima.core.search.Framework import Search, NodeExpander, Node

__author__ = 'Ivan Mushketik'

class CutOffIndicatorAction(Action):
    def is_noop(self):
        return True

CUT_OFF = CutOffIndicatorAction()

# Artificial Intelligence A Modern Approach (3rd Edition): Figure 3.17, page 88

 # function DEPTH-LIMITED-SEARCH(problem, limit) returns a solution, or failure/cutoff
 #   return RECURSIVE-DLS(MAKE-NODE(problem.INITIAL-STATE), problem, limit)
 #
 # function RECURSIVE-DLS(node, problem, limit) returns a solution, or failure/cutoff
 #   if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
 #   else if limit = 0 then return cutoff
 #   else
 #       cutoff_occurred? <- false
 #       for each action in problem.ACTIONS(node.STATE) do
 #           child <- CHILD-NODE(problem, node, action)
 #           result <- RECURSIVE-DLS(child, problem, limit - 1)
 #           if result = cutoff then cutoff_occurred? <- true
 #           else if result != failure then return result
 #       if cutoff_occurred? then return cutoff else return failure
class DepthFirstSearch(Search):

    def __init__(self, queueSearch):
        self._search = queueSearch

    def search(self, problem):
        pass

    def get_metrics(self):
        return self._search.get_metrics()
    
class DepthLimitedSearch(NodeExpander, Search):
    PATH_COST = "pathCost"

    def __init__(self, limit):
        super().__init__()
        self._limit = limit

    def is_cutoff(self, result):
        """
            Check if search ended because of cutoff.

            result - result of limited DFS
            return True if cutoff occurred, or False otherwise
        """
        return (len(result) == 1) and (result[0] == CUT_OFF)

    def is_failure(self, result):
        """
            Check if search ended because of failure.

            result - result of limited DFS
            return True if failure occurred, or False otherwise
        """
        return len(result) == 0

    def clear_instrumentation(self):
        super().clear_instrumentation()
        self._metrics[DepthLimitedSearch.PATH_COST] = 0

    def get_path_cost(self):
        return self._metrics[DepthLimitedSearch.PATH_COST]

    def set_path_cost(self, path_cost):
        self._metrics[DepthLimitedSearch.PATH_COST] = path_cost

    def search(self, problem):
        """
            Search solution for a problem with Depth First Search strategy with a specified depth limit.

            problem - problem to find solution for
            returns list of actions to execute from initial state to reach goal state. If search failed return a list that
            represents failure. If search ended because of cutoff returns a list that represents that cutoff occurred
        """

        # return RECURSIVE-DLS(MAKE-NODE(INITIAL-STATE[problem]), problem, limit)
        return self._recursive_dls(Node(problem.get_initial_state()), problem, self._limit)

    def _recursive_dls(self, curNode, problem, limit):
        goalTest = problem.get_goal_test()
        # if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
        if goalTest.is_goal_state(curNode.get_state()):
            self.set_path_cost(curNode.get_path_cost())
            return curNode.get_path_from_root()
        elif limit == 0:
            # else if limit = 0 then return cutoff
            return self._cutoff()
        else:
            # else
			# cutoff_occurred? <- false
            childNodes = self.expand_node(curNode, problem)

            cutoff_occurred = False
            # for each action in problem.ACTIONS(node.STATE) do
            for node in childNodes:
                # child <- CHILD-NODE(problem, node, action)
				# result <- RECURSIVE-DLS(child, problem, limit - 1)
                result = self._recursive_dls(node, problem, limit - 1)

                # if result = cutoff then cutoff_occurred? <- true
                if self.is_cutoff(result):
                    cutoff_occurred = True
                elif not self.is_failure(result):
                    # else if result != failure then return result
                    return result

            # if cutoff_occurred? then return cutoff else return failure
            if cutoff_occurred:
                return self._cutoff()
            else:
                return self._failure()

    def _cutoff(self):
        """ Return array with a single action that represents that search ended because cut off occured """
        return (CUT_OFF,)

    def _failure(self):
        """ Return list that represents that search ended because of failure """
        return []