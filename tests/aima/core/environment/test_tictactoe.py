from aima.core.environment.tictactoe import TicTacToeBoard
from aima.core.util.datastructure import XYLocation

__author__ = 'proger'

import unittest

class TicTacToeBoardTest(unittest.TestCase):
    def test_equality(self):
        ttb1 = TicTacToeBoard()
        ttb2 = TicTacToeBoard()

        self.assertEquals(ttb1, ttb2)

        ttb1.markO(1, 1)
        self.assertNotEqual(ttb1, ttb2)

        ttb2.markO(1, 1)
        self.assertEqual(ttb1, ttb2)

    def test_get_number_of_marked_positions(self):
        ttb = TicTacToeBoard()
        self.assertEqual(0, ttb.get_number_of_marked_positions())

        ttb.markO(1, 2)
        ttb.markO(2, 1)
        ttb.markO(1, 2)
        self.assertEqual(2, ttb.get_number_of_marked_positions())

    def test_get_unmarked_positions(self):
        ttb = TicTacToeBoard()
        expected_positions = [XYLocation(0, 0), XYLocation(0, 1), XYLocation(0, 2),
                              XYLocation(1, 0), XYLocation(1, 1), XYLocation(1, 2),
                              XYLocation(2, 0), XYLocation(2, 1), XYLocation(2, 2)]
                
        self.assertSameElements(expected_positions, ttb.get_unmarked_positions())

        ttb.markO(1, 2)
        ttb.markX(0, 0)
        ttb.markO(2, 2)

        expected_positions = [                  XYLocation(0, 1), XYLocation(0, 2),
                              XYLocation(1, 0), XYLocation(1, 1), XYLocation(1, 2),
                              XYLocation(2, 0)]

        self.assertSameElements(expected_positions, ttb.get_unmarked_positions())

    def test_is_any_diagonal_complete(self):
        ttb = TicTacToeBoard()
        self.assertFalse(ttb.is_diagonal_complete())

        ttb.markX(0, 0)
        ttb.markX(1, 1)
        ttb.markX(2, 2)
        self.assertTrue(ttb.is_diagonal_complete())

        ttb.markO(1, 1)
        self.assertFalse(ttb.is_diagonal_complete())

    def test_is_any_column_complete(self):
        ttb = TicTacToeBoard()
        self.assertFalse(ttb.is_diagonal_complete())

        ttb.markX(0, 0)
        ttb.markX(0, 1)
        ttb.markX(0, 2)
        self.assertTrue(ttb.is_any_row_complete())

        ttb.markO(0, 1)
        self.assertFalse(ttb.is_any_row_complete())

    def test_is_any_row_complete(self):
        ttb = TicTacToeBoard()
        self.assertFalse(ttb.is_diagonal_complete())

        ttb.markX(0, 0)
        ttb.markX(1, 0)
        ttb.markX(2, 0)
        self.assertTrue(ttb.is_any_column_complete())

        ttb.markO(1, 0)
        self.assertFalse(ttb.is_any_column_complete())


if __name__ == '__main__':
    unittest.main()
