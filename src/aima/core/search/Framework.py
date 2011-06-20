'''
Created on Jun 19, 2011

@author: Ivan Mushketik
'''

# Artificial Intelligence A Modern Approach (3rd Edition): page 66
from abc import ABCMeta

class Action(metaclass=ABCMeta):

    def is_noop(self):
        raise NotImplementedError()
    

#  Artificial Intelligence A Modern Approach (3rd Edition): page 67.
class ActionFunction(metaclass=ABCMeta):

    def actions(self, state):
        """
            Return set of actions that is possible in a current state
            state - current state
        """
        raise NotImplementedError()

# Artificial Intelligence A Modern Approach (3rd Edition): page 67.
class ResultFunction(metaclass=ABCMeta):

    def result(self, state, action):
        """
            Return a state that results from doing action in a current state
            state - current state
            action - action to do

            return new state
        """
        raise NotImplementedError();

# Artificial Intelligence A Modern Approach (3rd Edition): page 67
class GoalTest(metaclass=ABCMeta):

    def is_goal_state(self, state):
        """
        Check if current state is a goal state
        Returns true if state is a goal state or false otherwise
        """
        raise NotImplementedError("GoalTest is an abstract class");


# Artificial Intelligence A Modern Approach (3rd Edition): page 68
class StepCostFunction(metaclass=ABCMeta):
    def c(self, state, action, newState):
        """
            Calculate cost of taking action to perform state changing.

            state - state from which action is to be performed
            action - action to be performed
            newState - state reached by performing an action

            return - cost of performing an action
        """
        raise NotImplementedError("StepCostFunction is an abstract class");


class DefaultStepCostFunction(StepCostFunction):

    def __init__(self):
        pass

    """
        Step cost function that returns 1 for every action
    """
    def c(self, state, action, newState):
        return 1


class Problem:
    def __init__(self, initialState, actionsFunction, resultFuntion, goalTest,
                        stepCostFunction=None):
        self._initialState = initialState
        self._actionsFunction = actionsFunction
        self._resultFunction = resultFuntion
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
    def g(self, node):
        """
        Return cost from the initial state to a current state.        
        """
        return node.get_path_cost()


class NodeExpander:
    METRIC_NODES_EXPANDED = "nodesExpanded"

    def __init__(self):
        self._metrics = {}
        self.clear_instrumentation()
            
    def clear_instrumentation(self):
        self._metrics[NodeExpander.METRIC_NODES_EXPANDED] = 0
        
    def getNodesExpanded(self):
        pass
       
    def getMetrics(self):
        return self.metrics
        
    def expand_node(self, node, problem):
        """

        """
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


class QueueSearch(NodeExpander):
    pass