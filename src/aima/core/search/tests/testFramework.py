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

    def testIsRootForNodeWithoutParent(self):
        n1 = Node("state1")
        self.assertTrue(n1.isRootNode(), "Node created without parent should be root")
        
    def testIsRootForNodeWithParent(self):
        n1 = Node("state1")
        n2 = Node("state2", 0, n1)
        
        self.assertTrue(n1.isRootNode(), "Node created without parent should be root")
        self.assertFalse(n2.isRootNode(), "Node created with parent node shouldn't be root")
        self.assertEqual(n1, n2.getParent(), "Node.getParent() is broken")
        
    def testGetTotalPathCost(self):
        n1 = Node("state1", 5)
        n2 = Node("state2", 10, n1)
        n3 = Node("state3", 15, n2)
                
        self.assertEqual(30, n3.getPathCost(), "Path cost should be sum of cost of all nodes from root to a current node")
        
    def testGetPathFromRoot(self):
        n1 = Node("state1", 5)
        n2 = Node("state2", 10, n1)
        n3 = Node("state3", 15, n2)
        
        path = n3.getPathFromRoot()
        self.assertEquals(3, len(path), "Length of path should be equal to a number of nodes from current node to a root")
        self.assertEquals(n1, path[0])
        self.assertEquals(n2, path[1])
        self.assertEquals(n3, path[2])
        
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()