from aima.core.search.csp import Selection, ImprovedBacktrackingStrategy, MapCSP

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

lcbs = ImprovedBacktrackingStrategy(Selection.MRV_DEG)

map_csp = MapCSP()
result = lcbs.solve(map_csp)
print(result)