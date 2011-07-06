from aima.core.search.csp import MinConflictsStrategy, MapCSP

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

__doc__ = """
 Example that show how MinConflictStrategy can be used to solve map coloring problem.
"""

NUMBER_OF_TRIES = 5
NUMBER_OF_STEPS = 60

mcs = MinConflictsStrategy(NUMBER_OF_STEPS)
map_csp = MapCSP()

for i in range(NUMBER_OF_TRIES):
    result = mcs.solve(map_csp)
    if result:
        print("Search succeeded")
        print(result)
    else:
        print("Search failed")

    print("\n")
