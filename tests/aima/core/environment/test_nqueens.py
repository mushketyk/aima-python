from aima.core.environment.nqueens import NQueensBoard, NQResultFunction, NQIActionsFunctions, QueenAction, NQCActionsFunction, NQueensConverter
from aima.core.util.datastructure import XYLocation

__author__ = 'proger'

import unittest

class NQueensBoardTest(unittest.TestCase):
    def test_create_board(self):
        size = 5
        nqb = NQueensBoard(size)

        for r in range(size):
            for c in range(size):
                self.assertFalse(nqb.queen_exists_at_square(r, c))

    def test_get_number_of_queens_on_board(self):
        size = 5
        queens = (XYLocation(1, 1), XYLocation(2, 4), XYLocation(3, 3))
        nqb = NQueensBoard(size)

        nqb.set_board(queens)
        self.assertEqual(3, nqb.get_number_of_queens_on_board())

    def test_add_queen_at(self):
        nqb = NQueensBoard(5)
        nqb.add_queen_at(XYLocation(3, 4))
        self.assertTrue(nqb.queen_exists_at_square(4, 3))

    def test_remove_queen_from(self):
        nqb = NQueensBoard(5)
        nqb.add_queen_at(XYLocation(3, 4))
        nqb.remove_queen_from(XYLocation(3, 4))

        self.assertEqual(0, len(nqb.get_queen_positions()))


    def test_get_number_of_attacking_pairs_d(self):
        size = 5
        queens = (XYLocation(1, 1), XYLocation(3, 3), XYLocation(0, 0))
        nqb = NQueensBoard(size)
        nqb.set_board(queens)

        self.assertEqual(3, nqb.get_number_of_attacking_pairs())

    def test_get_number_of_attacking_pairs_h(self):
        size = 5
        queens = (XYLocation(1, 1), XYLocation(3, 1), XYLocation(0, 1))
        nqb = NQueensBoard(size)
        nqb.set_board(queens)

        self.assertEqual(3, nqb.get_number_of_attacking_pairs())

    def test_get_number_of_attacking_pairs_v(self):
        size = 5
        queens = (XYLocation(1, 3), XYLocation(1, 4), XYLocation(1, 0))
        nqb = NQueensBoard(size)
        nqb.set_board(queens)

        self.assertEqual(3, nqb.get_number_of_attacking_pairs())


class NQResultFunctionTest(unittest.TestCase):
    def test_remove_queen_action(self):
        queens = (XYLocation(1, 3), XYLocation(1, 4), XYLocation(1, 0))
        nqb = NQueensBoard(5)
        nqb.set_board(queens)

        nqrf = NQResultFunction()
        new_board = nqrf.result(nqb, QueenAction(QueenAction.REMOVE_QUEEN, XYLocation(1, 4)))

        self.assertEquals(2, new_board.get_number_of_queens_on_board())

    def test_place_queen(self):
        nqb = NQueensBoard(5)

        nqrf = NQResultFunction()
        new_board = nqrf.result(nqb, QueenAction(QueenAction.PLACE_QUEEN, XYLocation(1, 2)))
        self.assertTrue(new_board.queen_exists_at_square(2, 1))

    def test_move_queen(self):
        nqb = NQueensBoard(5)
        nqb.add_queen_at(XYLocation(3, 4))

        nqrf = NQResultFunction()
        new_board = nqrf.result(nqb, QueenAction(QueenAction.MOVE_QUEEN, XYLocation(3, 1)))

        self.assertFalse(new_board.queen_exists_at_square(4, 3))
        self.assertTrue(new_board.queen_exists_at_square(1, 3))

class NQIActionsFunctionTest(unittest.TestCase):
    def test_actions(self):
        nqb = NQueensBoard(3)
        nqb.add_queen_at(XYLocation(0, 0))

        nqiaf = NQIActionsFunctions()
        actions = nqiaf.actions(nqb)
        expected_actions = [QueenAction(QueenAction.PLACE_QUEEN, XYLocation(1, 2)),
                            QueenAction(QueenAction.PLACE_QUEEN, XYLocation(2, 1))]
        self.assertSameElements(expected_actions, actions)

class NQCActionsFunctionTest(unittest.TestCase):
    def test_actions(self):
        nqb = NQueensBoard(3)
        nqb.add_queen_at(XYLocation(0, 0))
        nqb.add_queen_at(XYLocation(1, 1))
        nqb.add_queen_at(XYLocation(2, 2))

        nqcaf = NQCActionsFunction()
        actions = nqcaf.actions(nqb)
        expected_actions = [QueenAction(QueenAction.MOVE_QUEEN, XYLocation(0, 1)),
                            QueenAction(QueenAction.MOVE_QUEEN, XYLocation(0, 2)),
                            QueenAction(QueenAction.MOVE_QUEEN, XYLocation(1, 0)),
                            QueenAction(QueenAction.MOVE_QUEEN, XYLocation(1, 2)),
                            QueenAction(QueenAction.MOVE_QUEEN, XYLocation(2, 0)),
                            QueenAction(QueenAction.MOVE_QUEEN, XYLocation(2, 1))]
        self.assertSameElements(expected_actions, actions)

class NQStateConverterTest(unittest.TestCase):
    def test_get_length(self):
        length = 5
        conv = NQueensConverter(length)

        self.assertEqual(length, conv.get_individual_length())

    def test_get_alphabet(self):
        conv = NQueensConverter(5)
        expected_alphabet = ['0', '1', '2', '3', '4']

        self.assertSameElements(set(expected_alphabet), set(conv.get_alphabet()))

    def test_get_string(self):
        board = NQueensBoard(5)
        board.add_queen_at(XYLocation(0, 2))
        board.add_queen_at(XYLocation(1, 3))
        board.add_queen_at(XYLocation(2, 0))
        board.add_queen_at(XYLocation(3, 4))
        board.add_queen_at(XYLocation(4, 1))

        expected_string = "23041"
        conv = NQueensConverter(5)

        self.assertEqual(expected_string, conv.get_string(board))

    def test_get_state(self):
        string = "23041"
        conv = NQueensConverter(5)

        expected_board = NQueensBoard(5)
        expected_board.add_queen_at(XYLocation(0, 2))
        expected_board.add_queen_at(XYLocation(1, 3))
        expected_board.add_queen_at(XYLocation(2, 0))
        expected_board.add_queen_at(XYLocation(3, 4))
        expected_board.add_queen_at(XYLocation(4, 1))

        self.assertEqual(expected_board, conv.get_state(string))



if __name__ == '__main__':
    unittest.main()
