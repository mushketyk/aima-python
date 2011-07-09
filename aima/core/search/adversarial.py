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


class MinMaxSearch(AdversarialSearch):
    """
    Simple search algorithm.
    """
    def get_action(self, state):
        (cost, action) = self._max_value(state, 1, 0)
        return action

    def _max_value(self, state, probability, curr_level):
        if self.terminal_state(state):
            return self.utility_function(state)
        elif curr_level == self.max_level:
            return probability * self.utility_function(state)

        best_action = None
        maximum_value = MinusInfinity()
        for (state, action, probability) in self.successor_function.get_successor_states(state):
            value = self._min_value(state, probability, curr_level + 1)
            if value > maximum_value:
                maximum_value = value
                best_action = action

        return (maximum_value, best_action)


    def _min_value(self, state, probability, curr_level):
        if self.terminal_state(state):
            return self.utility_function(state)
        elif curr_level == self.max_level:
            return probability * self.utility_function(state)

        best_action = None
        minimum_value = PlusInfinity()
        for (state, action, probability) in self.successor_function.get_successor_states(state):
            value = self._min_value(state, probability, curr_level + 1)
            if value < minimum_value:
                minimum_value = value
                best_action = action

        return (minimum_value, best_action)


class AlphaBetaSearch(AdversarialSearch):
    def get_action(self, state):
        pass