from aima.core.agent import Agent
from aima.core.util.other import MinusInfinity, PlusInfinity

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

class UtilityFunction:
    def __call__(self, state):
        """
        Calculate utility of the current state

        :param state: current state
        :return (number): number that represents utility of the current state. The higher is utility the bigger should be
        number.
        """

        raise NotImplementedError()


class TerminalStateFunction:
    def __call__(self, state):
        """
        Check if current state is terminal

        :param state: current state
        :return (bool): True is current state is terminal, False otherwise
        """
        raise NotImplementedError()


class AdversarialSearch:
    def __init__(self, successor_function, utility_function, terminal_state_function, limit=PlusInfinity()):
        self.max_level = limit
        self.successor_function = successor_function
        self.utility_function = utility_function
        self.terminal_state = terminal_state_function

    def get_action(self, state):
        """
        Get best action in the current state

        :param state: current state
        :return (Action): action that should be performed
        """
        raise NotImplementedError()


class SuccessorFunction():
    def get_successor_states(self, state):
        """
        Get successors of a current state.

        :return list((state, action, probability)): list of tuples, and each tuple contains of a new state, action that
         need to be performed to reach new state from current state and probability of this action.
        """
        raise NotImplementedError()


class GameAgent(Agent):
    def __init__(self, search, successor_function, utility_function):
        super().__init__()
        self.search = search
        self.utility_function = utility_function
        self.successor_function = successor_function

    def execute(self, percept):
        action = self.search.get_action(percept)
        return action

# function Minimax_Decision(state) returns an action
#   inputs state, current state in game
#
#   v <- Max-Value(state)
#   return the action in Successors(state) with value v
#
# function Max-Value(state) returns a utility value
#   inputs: state, current state in game
#
#   if Terminal-Test(state) then return Utility(state)
#   v <- -Infinity
#   for a, s in Successors(state) do
#     v <- Max(v, Min-Value(s))
#   return v
#
# function Min-Value(state) returns a utility value
#   inputs: state, current state in game
#
#   if Terminal-Test(state) then return Utility(state)
#   v <- Infinity
#   for a, s in Successors(state) do
#     v <- Min(v, Max-Value(s))
#   return v
class MinMaxSearch(AdversarialSearch):
    """
    Simple search algorithm.
    """
    # function Minimax_Decision(state) returns an action
    #   inputs state, current state in game
    def get_action(self, state):
        self.best_action = None
        # v <- Max-Value(state)
        self._max_value(state, 1, 0)
        # return the action in Successors(state) with value v
        return self.best_action

    # function Max-Value(state) returns a utility value
    def _max_value(self, state, probability, curr_level):
        # if Terminal-Test(state) then return Utility(state)
        if self.terminal_state(state):
            return self.utility_function(state)
        elif curr_level == self.max_level:
            return probability * self.utility_function(state)

        # v <- -Infinity
        maximum_value = MinusInfinity()
        # for a, s in Successors(state) do
        for (state, action, probability) in self.successor_function.get_successor_states(state):
            # v <- Max(v, Min-Value(s))
            value = self._min_value(state, probability, curr_level + 1)
            if value > maximum_value:
                maximum_value = value
                self.best_action = action
        # return v
        return maximum_value


    # function Max-Value(state) returns a utility value
    def _min_value(self, state, probability, curr_level):
        # if Terminal-Test(state) then return Utility(state)
        if self.terminal_state(state):
            return self.utility_function(state)
        elif curr_level == self.max_level:
            return probability * self.utility_function(state)

        # v <- Infinity
        minimum_value = PlusInfinity()
        # for a, s in Successors(state) do
        for (state, action, probability) in self.successor_function.get_successor_states(state):
            # v <- Min(v, Max-Value(s))
            value = self._min_value(state, probability, curr_level + 1)
            if value < minimum_value:
                minimum_value = value

        # return v
        return minimum_value

# function Alpha-Beta-Search(state) returns an action
#   inputs state, current state in game
#
#   v <- Max-Value(state, -Infinity, +Infinity)
#   return the action in Successors(state) with value v
#
# function Max-Value(state, alpha, beta) returns a utility value
#   inputs: state, current state in game
#           alpha, the value of the best alternative for MAX along the path to state
#           beta, the value of the best alternative for MIN along the path to state
#
#   if Terminal-Test(state) then return Utility(state)
#   v <- -Infinity
#   for a, s in Successors(state) do
#     v <- Max(v, Min-Value(s))
#     if v >= beta then return v
#     alpha <- Max(alpha, v)
#   return v
#
# function Min-Value(state) returns a utility value
#   inputs: state, current state in game
#           alpha, the value of the best alternative for MAX along the path to state
#           beta, the value of the best alternative for MIN along the path to state
#   if Terminal-Test(state) then return Utility(state)
#   v <- Infinity
#   for a, s in Successors(state) do
#     v <- Min(v, Max-Value(s))
#     if v <= alpha then return v
#     beta = Min(beta, v)
#   return v
class AlphaBetaSearch(AdversarialSearch):
    # function Alpha-Beta-Search(state) returns an action
    #   inputs state, current state in game
    def get_action(self, state):
        self.best_action = None
        # v <- Max-Value(state, -Infinity, +Infinity)
        self._max_value(state, MinusInfinity(), PlusInfinity(), 1, 0)
        # return the action in Successors(state) with value v
        return self.best_action

    # function Max-Value(state, alpha, beta) returns a utility value
    #   inputs: state, current state in game
    #           alpha, the value of the best alternative for MAX along the path to state
    #           beta, the value of the best alternative for MIN along the path to state
    def _max_value(self, state, alpha, beta, probability, curr_level):
        # if Terminal-Test(state) then return Utility(state)
        if self.terminal_state(state):
            return self.utility_function(state)
        elif curr_level == self.max_level:
            return probability * self.utility_function(state)
        
        # v <- -Infinity
        maximum_value = MinusInfinity()
        # for a, s in Successors(state) do
        for (state, action, probability) in self.successor_function.get_successor_states(state):
            value = self._min_value(state, alpha, beta, probability, curr_level + 1)
            # v <- Max(v, Min-Value(s))
            if value > maximum_value:
                maximum_value = value
                self.best_action = action
            # if v >= beta then return v
            if value >= beta:
                return maximum_value
            #  alpha <- Max(alpha, v)
            alpha = max(alpha, maximum_value)

        # return v
        return maximum_value

    # function Min-Value(state) returns a utility value
    #   inputs: state, current state in game
    #           alpha, the value of the best alternative for MAX along the path to state
    #           beta, the value of the best alternative for MIN along the path to state
    def _min_value(self, state, alpha, beta, probability, curr_level):
        # if Terminal-Test(state) then return Utility(state)
        if self.terminal_state(state):
            return self.utility_function(state)
        elif curr_level == self.max_level:
            return probability * self.utility_function(state)
        # v <- Infinity
        minimum_value = PlusInfinity()
        # for a, s in Successors(state) do
        for (state, action, probability) in self.successor_function.get_successor_states(state):
            value = self._max_value(state, alpha, beta, probability, curr_level + 1)
            # v <- Min(v, Max-Value(s))
            if value < minimum_value:
                minimum_value = value
            # if v <= alpha then return v
            if value <= alpha:
                return minimum_value
            # beta = Min(beta, v)
            beta = min(beta, minimum_value)
        # return v
        return minimum_value
