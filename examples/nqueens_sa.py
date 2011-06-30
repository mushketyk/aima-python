from random import randint
from aima.core.environment.nqueens import AttackingPairHeuristic, NQueensBoard, NQIActionsFunctions, NQueensGoalTest, NQCActionsFunction, NQResultFunction
from aima.core.search.framework import Problem
from aima.core.search.local import SimulateAnnealingSearch
from aima.core.util.datastructure import XYLocation

__author__ = 'Ivan Mushketik'

##
# Example of using Simulate Annealing Search for solving NQueens problem. Every problem's state is a board
# where all N queens are set.
#

# Board size
SIZE = 5
NUMBER_OF_TESTS = 5

def main():
    for i in range(0, NUMBER_OF_TESTS):
        sa = SimulateAnnealingSearch(AttackingPairHeuristic())
        random_board = create_random_board()

        print("Test number: " + str(i))
        print("Random init board:")
        print(random_board)
        # Create N queen problem with N queens on the board
        p = Problem(random_board, NQCActionsFunction(), NQResultFunction(), NQueensGoalTest())
        # Search for a solution
        actions = sa.search(p)

        if not sa.failed():
            print("Test succeeded")
            print("Actions:")
            for action in actions:
                print(action)

        else:
            print("Search failed")

        print("Result state:")
        print(sa.last_state)
        print("\n\n")


def create_random_board():
    board = NQueensBoard(SIZE)

    for c in range(SIZE):
        r = randint(0, SIZE - 1)
        board.add_queen_at(XYLocation(c, r))

    return board

if __name__ == '__main__':
    main()



