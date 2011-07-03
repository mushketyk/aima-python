from random import randint
from aima.core.environment.nqueens import NQueensGoalTest, NQueensConverter, NQueensBoard, AttackingPairHeuristic
from aima.core.search.local import GeneticProblem, GeneticAlgorithm
from aima.core.util.datastructure import XYLocation

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

SIZE = 5
NUMBER_OF_TASKS = 2
NUMBER_OF_ITERATIONS = 100

def create_random_board():
    board = NQueensBoard(SIZE)

    for c in range(SIZE):
        r = randint(0, SIZE - 1)
        board.add_queen_at(XYLocation(c, r))

    return board

def main():
    for i in range(NUMBER_OF_TASKS):
        print("Iteration number " + str(i))

        boards = [create_random_board() for i in range(5)]
        print("Created boards:")
        for board in boards:
            print(str(board))
        print("\n")

        p = GeneticProblem(boards, NQueensGoalTest(), NQueensConverter(SIZE))
        ga = GeneticAlgorithm(0.1)
        best_state = ga.search(p, AttackingPairHeuristic(), 100)

        if ga.failed:
            print("Search Failed")
        else:
            print("Search Succeeded")
            
        print("Final state:")
        print(str(best_state))
        print("\n\n")

if __name__ == "__main__":
    main()