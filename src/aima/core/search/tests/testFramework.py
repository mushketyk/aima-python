'''
Created on Jun 19, 2011

@author: proger
'''
import unittest
import aima
import aima.core
import aima.core.search
from aima.core.search.Framework import *

class TestNode(unittest.TestCase):

    def test_is_root_for_node_without_parent(self):
        n1 = Node("state1")
        self.assertTrue(n1.is_root_node(), "Node created without parent should be root")
        
    def test_is_root_for_node_with_parent(self):
        n1 = Node("state1")
        n2 = Node("state2", 0, n1)
        
        self.assertTrue(n1.is_root_node(), "Node created without parent should be root")
        self.assertFalse(n2.is_root_node(), "Node created with parent node shouldn't be root")
        self.assertEqual(n1, n2.get_parent(), "Node.getParent() is broken")
        
    def test_get_total_path_cost(self):
        n1 = Node("state1", 5)
        n2 = Node("state2", 10, n1)
        n3 = Node("state3", 15, n2)
                
        self.assertEqual(30, n3.get_path_cost(), "Path cost should be sum of cost of all nodes from root to a current node")
        
    def test_get_path_from_root(self):
        n1 = Node("state1", 5)
        n2 = Node("state2", 10, n1)
        n3 = Node("state3", 15, n2)
        
        path = n3.get_path_from_root()
        self.assertEquals(3, len(path), "Length of path should be equal to a number of nodes from current node to a root")
        self.assertEquals(n1, path[0])
        self.assertEquals(n2, path[1])
        self.assertEquals(n3, path[2])

class TestAction(Action):
    def is_noop(self):
        return false

class TestActionsFunction(ActionFunction):
    def actions(self, state):
        res = []
        for i in range(0, 3):
            res.append(TestAction())

        return res

class TestResultFuntion(ResultFunction):
    def result(self, state, action):
        return state + 1

class TestGoalTest(GoalTest):
    def is_goal_state(self, state):
        return state == 3

class TestProblem(Problem):
    def __init__(self):
        super().__init__(1, TestActionsFunction(), TestResultFuntion(), TestGoalTest())


class TestNodeExpander(unittest.TestCase):
    def test_node_expanding(self):
        startNode = Node(1)
        problem = TestProblem()
        nodeExpander = NodeExpander()
        actionsList = nodeExpander.expand_node(startNode, problem)

        self.assertEqual(3, len(actionsList), "")
        self.assertEqual(2, actionsList[0].get_state())
        self.assertEqual(2, actionsList[1].get_state())
        self.assertEqual(2, actionsList[2].get_state())




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()