from aima.core.AgentImpl import NoOpAction

__author__ = 'Ivan Mushketik'

def actions_from_nodes(node_list):

    if len(node_list) == 1:
        return [NoOpAction()]
    else:
        actions = []
        for i in range(1, len(node_list)):
            node = node_list[i]
            actions.append(node.get_action())

        return actions

def is_goal_state(problem, node):
    gt = problem.get_goal_test()

    return gt.is_goal_state(node.get_state())

  