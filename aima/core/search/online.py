from aima.core.agent import Agent, NoOpAction
from aima.core.search.framework import DefaultStepCostFunction

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

class OnlineSearchProblem:
    def __init__(self, action_function, goal_test, step_cost_function = DefaultStepCostFunction()):
        self.action_function = action_function
        self.goal_test = goal_test
        self.step_cost_function = step_cost_function

    def is_goal_state(self, state):
        return self.goal_test.is_goal_state(state)


# Artificial Intelligence A Modern Approach (3rd Edition): Figure 4.21, page 150.
#
# function ONLINE-DFS-AGENT(s') returns an action
#   inputs: s', a percept that identifies the current state
#   persistent: result, a table, indexed by state and action, initially empty
#               untried, a table that lists, for each state, the actions not yet tried
#               unbacktracked, a table that lists, for each state, the backtracks not yet tried
#               s, a, the previous state and action, initially null
#
#   if GOAL-TEST(s') then return stop
#   if s' is a new state (not in untried) then untried[s'] <- ACTIONS(s')
#   if s is not null then
#       result[s, a] <- s'
#       add s to the front of the unbacktracked[s']
#   if untried[s'] is empty then
#       if unbacktracked[s'] is empty then return stop
#       else a <- an action b such that result[s', b] = POP(unbacktracked[s'])
#   else a <- POP(untried[s'])
#   s <- s'
#   return a
#
# Figure 4.21 An online search agent that uses depth-first exploration. The agent is
# applicable only in state spaces in which every action can be "undone" by some other action.<br>
class OnlineDFSAgent(Agent):
    def __init__(self, problem, pts_function):
        super().__init__()
        self._problem = problem
        self.init()
        self.pts_function = pts_function

    @property
    def problem(self):
        return self._problem

    @problem.setter
    def problem(self, problem):
        self._problem = problem
        self.init()

    def init(self):
        self.alive = True
        self.s = None
        self.a = None

        self.untried = {}
        self.unbacktracked = {}
        self.result = {}

    # function ONLINE-DFS-AGENT(s') returns an action
	# inputs: s', a percept that identifies the current state
    def execute(self, percept):
        s_prime = self.pts_function.get_state(percept)

        # if GOAL-TEST(s') then return stop
        if self._is_goal_state(s_prime):
            self.a = NoOpAction()
        else:
            # if s' is a new state (not in untried) then untried[s'] <- ACTIONS(s')
            if s_prime not in self.untried.keys():
                self.untried[s_prime] = self._actions(s_prime)

            # if s is not null then do
            if self.s != None:
                # Note: If I've already seen the result of this
				# [s, a] then don't put it back on the unbacktracked
				# list otherwise you can keep oscillating
				# between the same states endlessly.
                if s_prime != self.result.get((self.s, self.a)):
                    self.result[(self.s, self.a)] = s_prime

                    lst = self.unbacktracked.setdefault(s_prime, [])
                    lst.insert(0, self.s)

            # if untried[s'] is empty then
            if len(self.untried.get(s_prime)) == 0:
                if len(self.unbacktracked.get(s_prime)) == 0:
                    self.a = NoOpAction()
                else:
                    # else a <- an action b such that result[s', b] = POP(unbacktracked[s'])
                    popped = self.unbacktracked[s_prime].pop(0)
                    for (s, b) in self.result.keys():
                        if s == s_prime and self.result[(s, b)] == popped:
                            self.a = b
                            break
            else:
                # else a <- POP(untried[s'])
                self.a = self.untried[s_prime].pop(0)

        if self.a.is_noop():
            self.alive = False

        # s <- s'
        self.s = s_prime
        # return a
        return self.a

    def _is_goal_state(self, state):
        return self.problem.is_goal_state(state)

    def _actions(self, state):
        return self.problem.action_function.actions(state)


