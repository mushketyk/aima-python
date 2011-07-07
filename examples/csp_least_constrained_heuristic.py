
from aima.core.search.csp import ImprovedBacktrackingStrategy, Selection, Inference, MapCSP

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'


lcbs = ImprovedBacktrackingStrategy(Selection.DEFAULT_ORDER, Inference.NONE, True)

map_csp = MapCSP()
result = lcbs.solve(map_csp)
print(result)
