from aima.core.agent import EnvironmentView
from aima.core.environment.tictactoe import TicTacToeEnvironment
from aima.core.search.adversial import MinMaxSearch, GameAgent

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

class MovesListener(EnvironmentView):
    def agent_acted(self, agent, action, resulting_state):
        print("Agent: " + agent + "; Made move " + action)
        print("Result state is " + resulting_state)

def main():
    environment = TicTacToeEnvironment()
    environment.add_agent(GameAgent(MinMaxSearch()))


if __name__ == "__main__":
    main()