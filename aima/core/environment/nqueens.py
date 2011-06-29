from aima.core.agent import Action
from aima.core.search.framework import HeuristicFunction, GoalTest, ActionFunction, ResultFunction
from aima.core.util.datastructure import XYLocation

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

class NQueensBoard:
    """
    Queen board that represent state of the N-Queen board task. Each state is a square matrix with size N. Each element
    of the matrix contains either QUEEN or EMPTY. Element state can be accessed either by specifing number of row and column
    or by specifying (x, y) coordinates. X increases left to right and Y increases top to bottom with zero based index.
    """
    EMPTY = 0
    QUEEN = 1

    def __init__(self, size):
        self.squares = [ [0 for j in range(0, size)] for i in range(0, size)]
        self.size = size

    def clean(self):
        """
        Remove all queens from a board.

        :return: None
        """
        for r in range(0, self.size):
            for c in range(0, self.size):
                self.squares[r][c] = 0

    def set_board(self, locations):
        """
        Clean board and set queens in specified locations.

        :param locations (list of XYLocation): locatios to set queens to.
        :return: None
        """
        self.clean()
        for location in locations:
            self.add_queen_at(location)

    def add_queen_at(self, location):
        """
        Set queen in specified location.

        :param location (XYLocation): location to set queen into.
        :return: None
        """
        self.squares[location.y][location.x] = self.QUEEN

    def remove_queen_from(self, location):
        """
        Remove queen from specified location.

        :param location (XYLocation): location to remove queen from.
        :return: None
        """
        self.squares[location.y][location.x] = self.EMPTY

    def move_queen_to(self, location):
        """
        Remove all queens from row of specified location and put queen into it.

        :param location (XYLocation):
        :return: None
        """
        for r in range(0, self.size):
            self.squares[r][location.x] = self.EMPTY
        self.squares[location.y][location.x] = self.QUEEN

    def move_queen(self, from_location, to_location):
        """
        Move queen from location from_location to location to_location

        :param from_location (XYLocation): - location to move queen from
        :param to_location (XYLocation): - location to move queen to
        :return: None
        """
        if self.queen_exists_at(from_location) and (not self.queen_exists_at(to_location)):
            self.remove_queen_from(from_location)
            self.add_queen_at(to_location)

    def queen_exists_at(self, location):
        """
        Check if queen exists in specified location

        :param location (XYLocation):
        :return (bool): True if queen exists, False otherwise.
        """
        return self.squares[location.y][location.x] == self.QUEEN

    def queen_exists_at_square(self, r, c):
        """
        Check if queen exists in specified row, column.

        :param r (int): row
        :param c (int): column
        :return (bool): True if queen exists, False otherwise
        """
        return self.squares[r][c] == self.QUEEN

    def get_number_of_queens_on_board(self):
        """
        Return number of queens on a board

        :return (int): number of queens on a board
        """
        counter = 0

        for r in range(0, self.size):
            for c in range(0, self.size):
                if self.squares[r][c] == self.QUEEN:
                    counter += 1
        return counter

    def get_queen_positions(self):
        """
        Get positions of queens on a board

        :return (list of XYLocation): list of locations of queens
        """
        locations = []

        for r in range(0, self.size):
            for c in range(0, self.size):
                if self.squares[r][c] == self.QUEEN:
                    locations.append(XYLocation(c, r))
        return locations

    def get_number_of_attacking_pairs(self):
        """
        Get number of attacking pairs

        :return (int): number of attacking pairs
        """
        result = 0
        for location in self.get_queen_positions():
            result += self.get_number_of_attacks_on(location)

        return result / 2

    def get_number_of_attacks_on(self, location):
        """
        Get number of queens attacking on a specified location

        :param location (XYLocation):
        :return (int): number of attacking queens
        """
        return self.number_of_horizontal_attacks_on(location) + self.number_of_vertical_attacks_on(location) + \
               self.number_of_diagonal_attacks_on(location)

    def is_square_under_attack(self, location):
        """
        Check if square is under attack of other queen

        :param location (XYLocation): location to check
        :return (bool): True if location is under attack, False otherwise
        """
        return self.is_square_horizontally_attacked(location) or self.is_square_vertically_attacked(location) or \
               self.is_square_diagonally_attacked(location)

    def is_square_horizontally_attacked(self, location):
        return self.number_of_horizontal_attacks_on(location) > 0

    def is_square_vertically_attacked(self, location):
        return self.number_of_vertical_attacks_on(location) > 0

    def is_square_diagonally_attacked(self, location):
        return self.number_of_diagonal_attacks_on(location) > 0

    def number_of_horizontal_attacks_on(self, location):
       cnt = 0

       for c in range(self.size):
           if self.queen_exists_at_square(location.y, c) and c != location.x:
               cnt += 1

       return cnt

    def number_of_vertical_attacks_on(self, location):
       cnt = 0

       for r in range(self.size):
           if self.queen_exists_at_square(r, location.x) and r != location.y:
               cnt += 1

       return cnt

    def number_of_diagonal_attacks_on(self, location):
        cnt = 0

        x = location.x + 1
        y = location.y - 1
        while x < self.size and y > -1:
            if self.squares[y][x] == self.QUEEN:
                cnt += 1
            x += 1
            y -= 1

        x = location.x + 1
        y = location.y + 1
        while x < self.size and y < self.size:
            if self.squares[y][x] == self.QUEEN:
                cnt += 1
            x += 1
            y += 1

        x = location.x - 1
        y = location.y - 1
        while x > -1 and y > -1:
            if self.squares[y][x] == self.QUEEN:
                cnt += 1
            x -= 1
            y -= 1

        x = location.x - 1
        y = location.y + 1
        while x > -1 and y < self.size:
            if self.squares[y][x] == self.QUEEN:
                cnt += 1
            x -= 1
            y += 1

        return cnt

    def get_board_pic(self):
        """
        Get textual image of a queen board

        :return (str): textual image of a queen board
        """
        str = ""
        for r in range(self.size):
            for c in range(self.size):
                if self.squares[r][c] == self.QUEEN:
                    str += " Q "
                else:
                    str += " - "
            str += '\n'

        return str

    def __str__(self):
        return self.get_board_pic()


class AttackingPairHeuristic(HeuristicFunction):
    def h(self, board):
        return board.get_number_of_attacking_pairs()


class NQueensGoalTest(GoalTest):
    def is_goal_state(self, board):
        return board.size == board.get_number_of_queens_on_board() and \
               board.get_number_of_attacking_pairs() == 0

class QueenAction(Action):
    PLACE_QUEEN = "placeQueenAt"
    REMOVE_QUEEN = "removeQueenAt"
    MOVE_QUEEN = "moveQueenTo"

    def __init__(self, type, location):
        super().__init__(type)
        self.type = type
        self.location = location
        self.x = location.x
        self.y = location.y

    def __eq__(self, other):
        if not isinstance(other, QueenAction):
            return False

        return other.x == self.x and other.y == self.y and other.type == self.type

    def __str__(self):
        return "QueenAction('" + self.type + "', " + self.x + ", " + self.y + ")"

class NQIActionsFunctions(ActionFunction):
    """
    Action function that list actions, where each action puts a new queen in a square that isn't under attack
    """
    def actions(self, board):
        actions = []
        for r in range(board.size):
            for c in range(board.size):
                location = XYLocation(c, r)
                if not board.is_square_under_attack(location) and not board.queen_exists_at(location):
                    actions.append(QueenAction(QueenAction.PLACE_QUEEN, XYLocation(c, r)))

        return actions


class NQCActionsFunction(ActionFunction):
    """
    Action function that generates list of action, and each action is a movement of a queen along queen's column.
    This function is assumed to be used when all queens are set at once (local search).
    """
    def actions(self, board):
        actions = []
        for r in range(board.size):
            for c in range(board.size):
                location = XYLocation(c, r)
                if not board.queen_exists_at(location):
                    actions.append(QueenAction(QueenAction.MOVE_QUEEN, location))

        return actions


class NQResultFunction(ResultFunction):
    def result(self, board, action):
        new_board = NQueensBoard(board.size)
        new_board.set_board(board.get_queen_positions())

        if action.type == QueenAction.PLACE_QUEEN:
            new_board.add_queen_at(action.location)
        elif action.type == QueenAction.REMOVE_QUEEN:
            new_board.remove_queen_from(action.location)
        elif action.type == QueenAction.MOVE_QUEEN:
            new_board.move_queen_to(action.location)

        return new_board
