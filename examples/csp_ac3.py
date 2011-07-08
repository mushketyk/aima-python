from aima.core.search.csp import Selection, ImprovedBacktrackingStrategy, Inference, MapCSP

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'


lcbs = ImprovedBacktrackingStrategy(Selection.DEFAULT_ORDER, Inference.AC3)

map_csp = MapCSP()
result = lcbs.solve(map_csp)
print(result)