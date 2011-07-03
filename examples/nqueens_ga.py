from random import randint
from aima.core.environment.nqueens import NQueensGoalTest, NQueensConverter, NQueensBoard, AttackingPairHeuristic
from aima.core.search.local import GeneticProblem, GeneticAlgorithm
from aima.core.util.datastructure import XYLocation

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

SIZE = 5
NUMBER_OF_TASKS = 20
NUMBER_OF_ITERATIONS = 100

def create_random_board():
    board = NQueensBoard(SIZE)

    for c in range(SIZE):
        r = randint(0, SIZE - 1)
        board.add_queen_at(XYLocation(c, r))

    return board

def main():
    succeeded = 0
    for i in range(NUMBER_OF_TASKS):
        print("Iteration number " + str(i))

        boards = [create_random_board() for i in range(50)]
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
            succeeded += 1
            
        print("Final state:")
        print(str(best_state))
        print("\n\n")

    print("Succeeded " + str(succeeded) + "/" + str(NUMBER_OF_TASKS))

if __name__ == "__main__":
    main()