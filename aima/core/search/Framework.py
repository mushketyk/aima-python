from abc import ABCMeta
from aima.core.AgentImpl import CutOffIndicatorAction
from aima.core.search import Utils
from aima.core.util.Datastructure import PriorityQueue

__author__ = 'Ivan Mushketik'

#  Artificial Intelligence A Modern Approach (3rd Edition): page 67.
class ActionFunction(metaclass=ABCMeta):

    ##
    # Return set of actions that is possible in a current state
    # @param state - current state
    def actions(self, state):
        raise NotImplementedError()

# Artificial Intelligence A Modern Approach (3rd Edition): page 67.
class ResultFunction(metaclass=ABCMeta):

    ##
    # Return a state that results from doing action in a current state
    # @param state - current state
    # @param action - action to do
    #
    # @return new state
    def result(self, state, action):
        raise NotImplementedError()

# Artificial Intelligence A Modern Approach (3rd Edition): page 67
class GoalTest(metaclass=ABCMeta):

    ##
    # Check if current state is a goal state
    # @return True if state is a goal state or False otherwise
    def is_goal_state(self, state):
        raise NotImplementedError("GoalTest is an abstract class")


# Artificial Intelligence A Modern Approach (3rd Edition): page 68
class StepCostFunction(metaclass=ABCMeta):
    ##
    # Calculate cost of taking action to perform state changing.
    #
    # @param state - state from which action is to be performed
    # @param action - action to be performed
    # @param newState - state reached by performing an action
    #
    # @return cost of performing an action
    def c(self, state, action, newState):
        raise NotImplementedError("StepCostFunction is an abstract class")


class DefaultStepCostFunction(StepCostFunction):
    """
        Step cost function that returns 1 for every action
    """
    def __init__(self):
        pass

    def c(self, state, action, newState):
        return 1


class Problem:
    def __init__(self, initialState, actionsFunction, resultFunction, goalTest,
                        stepCostFunction=None):
        self._initialState = initialState
        self._actionsFunction = actionsFunction
        self._resultFunction = resultFunction
        self._goalTest = goalTest

        if stepCostFunction is not None:
            self._stepCostFunction = stepCostFunction
        else:
            self._stepCostFunction = DefaultStepCostFunction()

    def get_initial_state(self):
        return self._initialState

    def is_goal_state(self, state):
        return self._goalTest.isGoalTest(state)

    def get_goal_test(self):
        return self._goalTest

    def get_action_function(self):
        return self._actionsFunction

    def get_result_function(self):
        return self._resultFunction

    def get_step_cost_function(self):
        return self._stepCostFunction

# Artificial Intelligence A Modern Approach (3rd Edition): Figure 3.10, page 79
class Node:
    """
    Node that is created during search in state space. Each node refers a state in a state space, parent node,
    path cost of reaching this node's state and action that was done to explore this node's state.
    """
    def __init__(self, state, stepCost=0, parent=None, action=None):
        self._state = state        
        self._parent = parent
        self._action = action
        
        if parent is not None:
            self._pathCost = parent._pathCost + stepCost
        else:
            self._pathCost = stepCost
            
    def get_state(self):
        return self._state
            
    def get_parent(self):
        return self._parent
            
    def get_action(self):
        return self._action
    
    def get_path_cost(self):
        return self._pathCost
    
    def is_root_node(self):
        return self._parent is None

    ##
    # Get nodes that were explored to reach current node
    #
    # @return list of nodes from root node to a current one.
    def get_path_from_root(self):
        node = self;
        path = []
        
        while node is not None:
            path.insert(0, node)
            node = node.get_parent()
        
        return path
    
    def __str__(self):
        return ""          


# Artificial Intelligence A Modern Approach (3rd Edition): page 78.
class PathCostFunction:
    ##
    # Return cost from the initial state to a current state.
    #
    # @param node - node to calculate path cost for
    # @return Something
    def g(self, node):
        """
        """
        return node.get_path_cost()


class NodeExpander:
    METRIC_NODES_EXPANDED = "nodesExpanded"

    def __init__(self):
        self._metrics = {}
        self._metrics[NodeExpander.METRIC_NODES_EXPANDED] = 0
            
    def clear_instrumentation(self):
        self._metrics[NodeExpander.METRIC_NODES_EXPANDED] = 0
        
    def get_nodes_expanded(self):
        return self._metrics[NodeExpander.METRIC_NODES_EXPANDED]
       
    def get_metrics(self):
        return self._metrics

    ##
    # Expand a node and return nodes with states that are reachable from a current node
    #
    # @param node - node to explore
    # @return list of nodes with reachable states
    def expand_node(self, node, problem):
        childNodes = []

        currentState = node.get_state()
        actionFunction = problem.get_action_function()
        resultFunction = problem.get_result_function()
        stepCostFunction = problem.get_step_cost_function()

        for action in actionFunction.actions(currentState):
            newState = resultFunction.result(currentState, action)
            cost = stepCostFunction.c(currentState, action, newState)
            newNode = Node(newState, cost, node, action)

            childNodes.append(newNode)

        self._metrics[NodeExpander.METRIC_NODES_EXPANDED] = self._metrics[NodeExpander.METRIC_NODES_EXPANDED] + 1
        return childNodes


class Search(metaclass=ABCMeta):
    def search(self, problem):
        raise NotImplementedError()

    ##
    # Get metrics collected during search run
    #
    # @return dict with metrics
    def get_metrics(self):
        raise NotImplementedError()

    ##
    # Check if search ended because of cutoff
    #
    # @param result - result of a search
    # @return True if cutoff occurred, False otherwise
    def is_cutoff(self, result):
        return (len(result) == 1) and (result[0] == CutOffIndicatorAction())

    ##
    #   Check if search ended because of failure.
    #
    #   @param result - result of limited DFS
    #   @return True if failure occurred, or False otherwise
    def is_failure(self, result):
        return len(result) == 0

    def _cutoff(self):
        """ Return array with a single action that represents that search ended because cut off occured """
        return (CutOffIndicatorAction(),)

    def _failure(self):
        """ Return list that represents that search ended because of failure """
        return []

class QueueSearch(NodeExpander, Search):
    """
        Many searches in state space can be implemented with help adding new nodes to a queue, that implements
        certain discipline and popping old nodes from this queue to check if node's state is a goal one.
        This class is a base class for this kind of searches
    """
    METRIC_QUEUE_SIZE = "queueSize"
    METRIC_MAX_QUEUE_SIZE = "maxQueueSize"
    METRIC_PATH_COST = "pathCost"


    def __init__(self):
        super().__init__()
        self._check_goal_before_adding_to_frontier = False
        self._frontier = None
        
        self._metrics[self.METRIC_QUEUE_SIZE] = 0
        self._metrics[self.METRIC_PATH_COST] = 0
        self._metrics[self.METRIC_MAX_QUEUE_SIZE] = 0

    ##
    # Search for a solution saving new expanded nodes to a queue.
    # @param problem - problem to solve
    # @param frontier - Datastructures.Queue that implements certain discipline
    #
    # @return If solution was found return a list of actions to reach goal state from an initial state. If
    # initial state is a goal state this method returns a list with a NoOpAction. If failed to find a solution
    # it returns an empty list.
    def search(self, problem, frontier):
        self._frontier = frontier
        self.clear_instrumentation()

        root = Node(problem.get_initial_state())
        # check root node before adding to a queue
        if self._check_goal_before_adding_to_frontier:
            if Utils.is_goal_state(problem, root):
                self._set_path_cost(root.get_path_cost())
                return Utils.actions_from_nodes(root.get_path_from_root())

        self._add_to_frontier(root)
        self._set_new_queue_size()
        # while frontier isn't empty there are still states to check
        while not self._frontier.is_empty():
            node_to_expand  = self._pop_node_from_frontier()
            self._set_new_queue_size()

            # if state shouldn't be checked before adding it's time to check it now
            if not self._check_goal_before_adding_to_frontier:
                if Utils.is_goal_state(problem, node_to_expand):
                    self._set_path_cost(node_to_expand.get_path_cost())
                    return Utils.actions_from_nodes(node_to_expand.get_path_from_root())

            # Get new nodes, check them and add to a frontier
            for fn in self.get_resulting_nodes_to_add_to_frontier(node_to_expand, problem):
                if self._check_goal_before_adding_to_frontier:
                    if Utils.is_goal_state(problem, fn):
                        self._set_path_cost(fn.get_path_cost())
                        return Utils.actions_from_nodes(fn.get_path_from_root())

                self._add_to_frontier(fn)

            self._set_new_queue_size()

        # if we are here, all frontier is empty and a goal state wasn't found. Search failed
        return self._failure()

    def is_check_goal_before_adding_to_frontier(self):
        return self._check_goal_before_adding_to_frontier

    def set_check_goal_before_adding_to_frontier(self, check_before_adding):
        self._check_goal_before_adding_to_frontier = check_before_adding

    def get_resulting_nodes_to_add_to_frontier(self, node_to_expand, problem):
        raise NotImplementedError("Queue search is an abstract class")

    def clear_instrumentation(self):
        super().clear_instrumentation()
        self._metrics[self.METRIC_QUEUE_SIZE] = 0
        self._metrics[self.METRIC_PATH_COST] = 0
        self._metrics[self.METRIC_MAX_QUEUE_SIZE] = 0

    def _set_new_queue_size(self):
        size = self._frontier.length()
        self._metrics[self.METRIC_QUEUE_SIZE] = size

        max_size = self._metrics[self.METRIC_MAX_QUEUE_SIZE]
        if size > max_size:
            self._metrics[self.METRIC_MAX_QUEUE_SIZE] = size

    def get_queue_size(self):
        return self._metrics[self.METRIC_QUEUE_SIZE]

    def get_max_queue_size(self):
        return self._metrics[self.METRIC_MAX_QUEUE_SIZE]

    def _set_path_cost(self, path_cost):
        self._metrics[self.METRIC_PATH_COST] = path_cost

    def get_path_cost(self):
        return self._metrics[self.METRIC_PATH_COST]

    def _pop_node_from_frontier(self):
        return self._frontier.pop()

    def _remove_node_from_frontier(self, to_remove):
        return self._frontier.remove(to_remove)

    def _add_to_frontier(self, to_add):
        self._frontier.add(to_add)
        
 # Artificial Intelligence A Modern Approach (3rd Edition): Figure 3.7, page 77.
 # function TREE-SEARCH(problem) returns a solution, or failure
 #   initialize the frontier using the initial state of the problem
 #   loop do
 #     if the frontier is empty then return failure
 #     choose a leaf node and remove it from the frontier
 #     if the node contains a goal state then return the corresponding solution
 #     expand the chosen node, adding the resulting nodes to the frontier
class TreeSearch(QueueSearch):
    """
        Simple implementation of QueueSearch.
        New node is added to frontier no matter if it was found earlier or not.
    """
    def __init__(self):
        super().__init__()

    def get_resulting_nodes_to_add_to_frontier(self, node_to_expand, problem):
        return self.expand_node(node_to_expand, problem)


 # Artificial Intelligence A Modern Approach (3rd Edition): Figure 3.7, page 77.
 #
 # function GRAPH-SEARCH(problem) returns a solution, or failure
 #   initialize the frontier using the initial state of problem
 #   initialize the explored set to be empty
 #   loop do
 #     if the frontier is empty then return failure
 #     choose a leaf node and remove it from the frontier
 #     if the node contains a goal state then return the corresponding solution
 #     add the node to the explored set
 #     expand the chosen node, adding the resulting nodes to the frontier
 #       only if not in the frontier or explored set
 #
 # Figure 3.7 An informal description of the general graph-search algorithm.
class GraphSearch(QueueSearch):
    """
        When this search expand a node it checks if new node's state was explored before. If it was already explored
        new node doesn't added to frontier.
    """
    def __init__(self):
        super().__init__()
        self._explored = set([])
        self._frontier_state = {}
        self._comparator = None

    def get_node_comparator(self):
        return self._comparator

    def set_node_comparator(self, comparator):
        self._comparator = comparator

    def search(self, problem, frontier):
        self._explored = set([])
        self._frontier_state = {}
        return super().search(problem, frontier)

    def _pop_node_from_frontier(self):
        to_remove = super()._pop_node_from_frontier()
        if to_remove.get_state() in self._frontier_state.keys():
            del self._frontier_state[to_remove.get_state()]
        return to_remove

    def _remove_node_from_frontier(self, to_remove):
        removed = super()._remove_node_from_frontier(to_remove)
        if removed:
            del self._frontier_state[to_remove.get_state()]

        return removed

    def get_resulting_nodes_to_add_to_frontier(self, node_to_expand, problem):
        add_to_frontier = []
        self._explored.add(node_to_expand.get_state())

        for cfn in self.expand_node(node_to_expand, problem):
            yes_add_to_frontier = False

            # If node wasn't expanded before - add it to frontier
            if cfn.get_state() not in self._frontier_state.keys() and cfn.get_state() not in self._explored:
                yes_add_to_frontier = True
            # If node was expanded and we want to replace nodes with a smaller state cost ...
            elif cfn.get_state() in self._frontier_state.keys() and self._comparator != None:
                frontier_node = self._frontier_state[cfn.get_state()]

                # ... and new node's state cost is less that old node's state cost ...
                if self._comparator(cfn, frontier_node) < 0:
                    # ... add it to frontier
                    yes_add_to_frontier = True

                    self._remove_node_from_frontier(frontier_node)

                    add_to_frontier.remove(frontier_node)

            if yes_add_to_frontier:
                add_to_frontier.append(cfn)
                self._frontier_state[cfn.get_state()] = cfn

        return add_to_frontier


class PrioritySearch(Search):
    """
        Base class for searches that use priority queues in queue searches.
    """
    def __init__(self, queue_search):
        self._search = queue_search
        super().__init__()

    def search(self, problem):
        comparator = self._get_comparator()

        if isinstance(self._search, GraphSearch):
            self._search.set_node_comparator(comparator)

        return self._search.search(problem, PriorityQueue(comparator))

    def _get_comparator(self):
        """
            Get comparator that is used to compare nodes
        """
        raise NotImplementedError()

# Artificial Intelligence A Modern Approach (3rd Edition): page 92
class EvaluationFunction(metaclass=ABCMeta):
    def f(self, node):
        raise NotImplementedError()

# Artificial Intelligence A Modern Approach (3rd Edition): page 92
class HeuristicFunction(metaclass=ABCMeta):
    def h(self, state):
        raise NotImplementedError()