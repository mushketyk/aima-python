from aima.core.agent import EnvironmentView
from aima.core.environment.tictactoe import TicTacToeEnvironment, TicTacToeSuccessorFunction, TicTacToeUtilityFunction, TicTacToeTerminalStateFunction
from aima.core.search.adversarial import MinMaxSearch, GameAgent

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

# Example of unsing eversarial search to create TicTacToe competition between to boots

# Listener that prints result of every move in the game
class MovesListener(EnvironmentView):
    def agent_acted(self, agent, action, resulting_state):
        print("Agent: " + str(agent) + "; Made move " + str(action))
        print("Result state is:\n" + str(resulting_state))

def main():
    # Create environment for TicTacToe
    environment = TicTacToeEnvironment()
    # Create two players. Each agent has it's own functions. Because each agent has own functions
    # this can help to test 
    x_agent = GameAgent(MinMaxSearch(TicTacToeSuccessorFunction(True),
                                     TicTacToeSuccessorFunction(False),
                                     TicTacToeUtilityFunction(True),
                                     TicTacToeTerminalStateFunction()))
    o_agent = GameAgent(MinMaxSearch(TicTacToeSuccessorFunction(False),
                                     TicTacToeSuccessorFunction(True),
                                     TicTacToeUtilityFunction(False),
                                     TicTacToeTerminalStateFunction()))

    # Add listener that shows each agent's action
    environment.add_environment_view(MovesListener())
    # Add agents
    environment.add_agent(x_agent)
    environment.add_agent(o_agent)
    # Set what agent sets X, and what agent sets O
    environment.x_agent = x_agent
    environment.o_agent = o_agent

    # Run game, until it's done
    environment.step_until_done()


if __name__ == "__main__":
    main()