from aima.core.environment.nqueens import NQueensGoalTest, NQResultFunction, NQIActionsFunctions, NQueensBoard
from aima.core.search.framework import TreeSearch, Problem
from aima.core.search.uninformed import DepthFirstSearch

__author__ = 'Ivan Mushketik'

##
# Example of solving N-queens problem with help of DFS

# Size of the chess board
SIZE = 5

# Using tree DFS
ts = TreeSearch()
dfs = DepthFirstSearch(ts)
# Create empty board
empty_board = NQueensBoard(SIZE)
# Define N-queen board
p = Problem(empty_board, NQIActionsFunctions(), NQResultFunction(), NQueensGoalTest())
# Get list of actions to solve a problem
actions = dfs.search(p)

board_to_show = NQueensBoard(SIZE)
rf = NQResultFunction()
# Print each action and perform each action (putting new queen on a board)
for action in actions:
    print(action)
    board_to_show = rf.result(board_to_show, action)

# Print result board
print(board_to_show)


    

