'''
Created on Jun 19, 2011

@author: Ivan Mushketik
'''
from aima.core.search.Framework import Search

class DepthFirstSearch(Search):

    def __init__(self, queueSearch):
        self._search = queueSearch

    def search(self, problem):
        pass

    def get_metrics(self):
        return self._search.get_metrics()
    
