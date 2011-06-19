'''
Created on Jun 19, 2011

@author: Ivan Mushketik
'''

class Node:
    def __init__(self, state, stepCost=0, parent=None, action=None):
        self._state = state        
        self._parent = parent
        self._action = action
        
        if parent is not None:
            self._pathCost = parent._pathCost + stepCost
        else:
            self._pathCost = stepCost
            
    def getState(self):
        return self._state
            
    def getParent(self):
        return self._parent
            
    def getAction(self):
        return self._action
    
    def getPathCost(self):
        return self._pathCost
    
    def isRootNode(self):
        return self._parent is None
    
    def getPathFromRoot(self):
        node = self;
        path = []
        
        while node is not None:
            path.insert(0, node)
            node = node.getParent()
        
        return path
    
    def __str__(self):
        return ""          
        
# Artificial Intelligence A Modern Approach (3rd Edition): page 67
class GoalTest:
    
    def isGoalState(self, state):
        """
        Check if current state is a goal state
        Returns true if state is a goal state or false otherwise
        """        
        raise NotImplementedError("GoalTest is an abstract class");

# Artificial Intelligence A Modern Approach (3rd Edition): page 68
class StepCostFunction:
    def c(self, state, action, newState):
        
        raise NotImplementedError("StepCostFunction is an abstract class");

# Artificial Intelligence A Modern Approach (3rd Edition): page 78.
class PathCostFunction:
    def g(self, node):
        """
        Return cost from the initial state to a current state.        
        """
        return node.getPathCost()
    
    
    
    
class NodeExpander:
    def __init__(self):
        self.metrics = {}
            
    def clearInstrumentation(self):
        pass
        
    def getNodesExpanded(self):
        pass
       
    def getMetrics(self):
        return self.metrics
        
    def expandNode(self, node, problem):
        pass
