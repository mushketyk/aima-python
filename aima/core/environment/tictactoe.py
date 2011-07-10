from aima.core.agent import Environment
from aima.core.search.adversarial import UtilityFunction, TerminalStateFunction, SuccessorFunction
from aima.core.util.datastructure import XYLocation

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

class TicTacToeBoard:
    """
    Tic-tac-toe board class that stores tic-tac-toe game state. State is stored as an 2-dimensional array.
    Each element of this array can be either O, or X, or empty
    """
    O = "O"
    X = "X"
    EMPTY = "_"

    def __init__(self):
        self.board = [[self.EMPTY, self.EMPTY, self.EMPTY] for i in range(3)]

    def is_empty(self, row, col):
        """
        Check if cell with specifed row and col is empty

        :param row (int):
        :param col (int:
        :return (bool): True if cell is empty, False otherwise
        """
        return self.board[row][col] == self.EMPTY

    def is_marked(self, value,  row, col):
        """
        Check if specifed cell contains specified value

        :param value {X, O, EMPTY}:
        :param row (int):
        :param col (int):
        :return (bool): True if cell is empty, False otherwise
        """
        return self.board[row][col] == value

    def markX(self, row, col):
        """
        Put X in specified cell

        :param row (int):
        :param col (int):
        """
        self.board[row][col] = self.X

    def markO(self, row, col):
        """
        Put O in specified cell

        :param row (int):
        :param col (int):
        """
        self.board[row][col] = self.O

    def is_any_column_complete(self):
        """
        Check if any column of the tic-tac-toe board is complete

        :return (bool): True if any column is complete, False otherwise
        """
        for i in range(3):
            val = self.board[0][i]
            if val != self.EMPTY and self.board[1][i] == val and self.board[2][i] == val:
                return True

        return False

    def is_any_row_complete(self):
        """
        Check if any row of the tic-tac-toe board is complete

        :return (bool): True if any row is complete, False otherwise
        """
        for i in range(3):
            val = self.board[i][0]
            if val != self.EMPTY and self.board[i][1] == val and self.board[i][2] == val:
                return True

        return False

    def is_diagonal_complete(self):
        """
        Check if any of tic-tac-toe diagonals is complete

        :return (bool): True if any diagoanl is complete, False otherwise
        """
        val = self.board[0][0]

        if val != self.EMPTY and self.board[1][1] == val and self.board[2][2] == val:
            return True

        val = self.board[0][2]
        if val != self.EMPTY and self.board[1][1] == val and self.board[2][0] == val:
            return True

        return False

    def get_value(self, row, col):
        """
        Get value from specified cell.

        :param row (int):
        :param col (int):
        :return {X, O, EMPTY}:
        """
        return self.board[row][col]

    def set_value(self, row, col, value):
        """
        Set value to the specified cell.

        :param row (int):
        :param col (int):
        :param value {X, O, EMPTY}:
        """
        self.board[row][col] = value

    def clone_board(self):
        """
        Create new board with the same state

        :return (TicTacToeBoard): clone of the current tic-tac-toe board
        """
        new_board = TicTacToeBoard()

        for r in range(3):
            for c in range(3):
                new_board.board[r][c] = self.board[r][c]

        return new_board

    def get_number_of_marked_positions(self):
        """
        Get number of not empty positions

        :return (int): number of not empty positions
        """
        number = 0

        for r in range(3):
            for c in range(3):
                if not self.is_empty(r, c):
                    number += 1

        return number

    def get_unmarked_positions(self):
        """
        Return coordinates of not empty positions

        :return list(XYPosition): coordinates of not empty positions on the board.
        """
        result = []

        for r in range(3):
            for c in range(3):
                if self.is_empty(r, c):
                    result.append(XYLocation(c, r))

        return result

    def line_through_board(self):
        return self.is_any_column_complete() or self.is_any_row_complete() or self.is_diagonal_complete()

    def __eq__(self, other):
        if not isinstance(other, TicTacToeBoard):
            return False

        for r in range(3):
            for c in range(3):
                if self.board[r][c] != other.board[r][c]:
                    return False

        return True

    def __str__(self):
        result = ""

        for r in range(3):
            for c in range(3):
                result += self.board[r][c]
            result += "\n"

        return result


class TicTacToeEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self.board = TicTacToeBoard()
        self.x_agent = None
        self.o_agent = None


    def execute_action(self, agent, action):
        if action != None:
            c = action.x
            r = action.y

            if agent == self.x_agent:
                self.board.markX(r, c)
            elif agent == self.o_agent:
                self.board.markO(r, c)

        return self.board

    def get_percept_seen_by(self, agent):
        return self.board

    def get_current_state(self):
        return self.board

class TicTacToeUtilityFunction(UtilityFunction):
    """
    VERY stupid utility function. But I am too lazy to write something better
    """

    def __init__(self, x_agent):
        if x_agent:
            self.agent_mark = TicTacToeBoard.X
        else:
            self.agent_mark = TicTacToeBoard.O

    def __call__(self, board):
        utility = 0

        for r in range(3):
            for c in range(3):
                value = board.get_value(r, c)
                if value != TicTacToeBoard.EMPTY:
                    if value == self.agent_mark:
                        utility += 1
                    else:
                        utility -= 1
        return utility

class TicTacToeTerminalStateFunction(TerminalStateFunction):
    """
    Terminal state function for tic-tac-toe
    """
    def __call__(self, board):
        return board.line_through_board()


class TicTacToeSuccessorFunction(SuccessorFunction):
    """
    Successor function for tic-tac-toe
    """
    def __init__(self, x_agent):
        if x_agent:
            self.agent_mark = TicTacToeBoard.X
        else:
            self.agent_mark = TicTacToeBoard.O

    def get_successor_states(self, board):
        if board.line_through_board():
            return []

        unmarked_positions = board.get_unmarked_positions()

        result = []
        for pos in unmarked_positions:
            new_board = board.clone_board()
            new_board.set_value(pos.y, pos.x, self.agent_mark)
            result.append((new_board, pos, 1))

        return result



