from random import random
from aima.core.util.datastructure import FIFOQueue, LIFOQueue
from aima.core.util.functions import normalize, rest, randbool

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

class ProbabilityDistribution:
    class Row:
        def __init__(self, probability, values):
            self.probability = probability
            self.values = tuple(values)

        def matches(self, var_pos, value):
            if var_pos != None:
                return self.values[var_pos] == value
            return False

        def __str__(self):
            return self.values + " => " + self.probability


    def __init__(self, variables):
        """
        :param variables iterable(str): names of all variables in this probability distribution
        """
        self.rows = []
        self.variables_places = {}

        i = 0
        for var in variables:
            self.variables_places[var] = i
            i += 1

    def set(self, probability, values):
        """
        Add probability of variables in probability distribution to have specified values.

        :param probability: probability of variables in this probability distribution have specified values
        :param values iterable(bool): values of variables
        :return: None
        """
        if len(values) != len(self.variables_places.keys()):
            raise ValueError("Invalid number of values. Should be equal to a number of variables")

        self.rows.append(self.Row(probability, values))

    def probability_of(self, conditions):
        """
        Calculate probability of specified conditions in current probability distribution.

        :param conditions table(str, bool): values
        :return (float): probability of specified conditions
        """
        prob = 0
        for row in self.rows:
            row_meets_all_conditions = True
            for var_name in conditions.keys():
                cond_value = conditions[var_name]

                variable_place = self.variables_places.get(var_name)
                if variable_place != None:
                    if not row.matches(variable_place, cond_value):
                        row_meets_all_conditions = False
                        break

            if row_meets_all_conditions:
                prob += row.probability

        return prob

class Query:
    def __init__(self, query_variable, evidence):
        self.query_variable = query_variable
        self.evidence = dict(evidence)
        
#  function Enumerate-Joint-Ask(X, e, P) returns a distribution over X
#    inputs: X, the query variable
#            e, observed values for variables E
#            P, a joint distribution on variables {X} U E U Y /* Y = hidden variables */
#
#    Q(X) <- a distribution over X, initially empty
#    for each value xi of X do
#       Q(xi) <- Enumerate-Joint(xi, e, Y, [], P)
#    return Normalize(Q(X))
#
#  function Enumerate-Joint(x, e, vars, values, P) returns a real number
#    if Empty?(vars) then return P(x, e, values)
#    Y <- First(vars)
#    return sum(Enumerate-Joint(x, e, Rest(vars), [y|values], P)
class EnumerationJointAsk:
    def ask(self, query, probability_distribution):
        """

        :param query (Query):
        :param probability_distribution (ProbabilityDistribution):
        :return (float, float):
        """
        h = dict(query.evidence)

        h[query.query_variable] = True
        true_distr = probability_distribution.probability_of(h)

        h[query.query_variable] = False
        false_distr = probability_distribution.probability_of(h)


        return normalize((true_distr, false_distr))

class Randomizer:
    def next_double(self):
        raise NotImplementedError("Randomizer is an abstract class")

class StandardRandomizer(Randomizer):
    def next_double(self):
        return random()

class BayesNetNode:
    """
    Node of Bayes network
    """
    def __init__(self, variable):
        self.variable = variable
        self.parents = []
        self.children = []
        self.distribution = ProbabilityDistribution([variable])

    def influenced_by(self, *parents):
        """
        Add nodes that influences current node in this network
        :param parents (BayesNetNode): nodes that influence this node.
        :return: None
        """
        for parent in parents:
            self._add_parent(parent)
            parent._add_child(self)

        self.distribution = ProbabilityDistribution((parent.variable for parent in parents))

    def set_probablity(self, probablity, values):
        """
        Set probability of values combination.

        :param probablity: probability of specified values combinations.
        :param values iterable(bool): values of the parent node. If current node is root, iterable should contain only one
         element: True or False.
        :return: None
        """
        if self.is_root():
            value = values[0]

            self.distribution.set(probablity, [value])
            self.distribution.set(1 - probablity, [not value])

        else:
            self.distribution.set(probablity, values)

    def probability_of(self, conditions):
        """
        Get probability of specified conditions.

        :param conditions hash(str, bool): hash table that specifies values of parent variables.
        :return (float): probability of specified conditions
        """
        return self.distribution.probability_of(conditions)

    def is_true_for(self, probability, model_build_up_so_far):
        conditions = {}
        if self.is_root():
            conditions = {self.variable : True}
        else:
            conditions = dict(model_build_up_so_far)

        true_probability = self.probability_of(conditions)

        if probability <= true_probability:
            return True
        else:
            return False

    def __str__(self):
        return "BayesNetNode(" + self.variable + ")"

    def __eq__(self, other):
        if not isinstance(other, BayesNetNode):
            return False

        return self.variable == other.variable

    def __hash__(self):
        return hash(self.variable)

    def _add_parent(self, parent):
        if not parent in self.parents:
            self.parents.append(parent)

    def _add_child(self, child):
        if not child in self.children:
            self.children.append(child)

    def is_root(self):
        return len(self.parents) == 0


class BayesNet:
    def __init__(self, roots):
        self.roots = tuple(roots)
        self.variable_nodes = None

    def get_variables(self):
        var_nodes = self._get_variable_nodes()

        return [node.variable for node in var_nodes]

    def probability_of(self, var_name, value, evidence):
        var_node = self._get_node_of(var_name)

        if var_node == None:
            raise ValueError("Unable to find a node with variable " + var_name)
        else:
            if var_node.is_root():
                var_table = {var_name: value}
                return var_node.probability_of(var_table)
            else:
                parent_values = {parent.variable : evidence[parent.variable] for parent in var_node.parents}

                probability = var_node.probability_of(parent_values)

                if value:
                    return probability
                else:
                    return 1 - probability

    # function PriorSample(bn) returns an event sampled from the prior specified by bn
    #   inputs: bn, a Bayesian network specifying joint distribution P(X1,..., Xn)
    #
    #   x <- an event with n elements
    #   for i = 1 to n do
    #     xi <- a random sample from P(Xi | parents(Xi))
    #   return x
    #
    # A sampling algorithm that generates events from a Bayesian network
    def get_prior_sample(self, randomizer=StandardRandomizer()):
        h = {}
        for node in self._get_variable_nodes():
            h[node.variable] = node.is_true_for(randomizer.next_double(), h)

        return h

    def _get_variable_nodes(self):
        if self.variable_nodes == None:
            new_variables_nodes = []
            parents = list(self.roots)
            traversed_parents = []

            while len(parents) != 0:
                new_parents = []
                for parent in parents:
                    if parent not in traversed_parents:
                        new_variables_nodes.append(parent)

                        for child in parent.children:
                            if child not in new_parents:
                                new_parents.append(child)

                        traversed_parents.append(parent)
                parents = new_parents
            self.variable_nodes = new_variables_nodes


        return self.variable_nodes

    def _get_node_of(self, var_name):
        for node in self._get_variable_nodes():
            if node.variable == var_name:
                return node
            
        return None
            
#  function EnumerationAsk(X, e, bn) returns a distribution over X
#    inputs: X, the query variable
#            e, observed values for variables E
#            bn, a Bayes net with variables {X} U E U Y /* Y - hidden variables */
#    
#    Q(X) <- a distribution over X, initially empty
#    for each value xi of X do
#      extend e with value xi for X
#      Q(xi) <- EnumerateAll(Vars[bn], e)
#    return Normalize(Q(X))
#
#  function EnumerateAll(vars, e) return a real numer
#    if Empty?(vars) then return 1.0
#      Y <- First(vars)
#    if Y has value y in e
#      then return P(y | parents(Y)) * EnumerateAll(Rest(vars), e)
#      else return SUMy P(y | paretns(Y)) * EnumerateAll(vars), ey)
#          where ey is e extended with Y = y
class EnumerationAsk:
    def ask(self, query, bayes_net):
        evidence_vars = dict(query.evidence)

        evidence_vars[query.query_variable] = True
        true_probability = self._enumerate_all(bayes_net, bayes_net.get_variables(), evidence_vars)

        evidence_vars[query.query_variable] = False
        false_probability = self._enumerate_all(bayes_net, bayes_net.get_variables(), evidence_vars)

        return normalize((true_probability, false_probability))

    def _enumerate_all(self, bayes_net, unprocessed_variables, evidence_variables):
        if len(unprocessed_variables) == 0:
            return 1
        else:
            var = unprocessed_variables[0]
            if var in evidence_variables.keys():
                prob_var_true_given_parents = bayes_net.probability_of(var, evidence_variables[var], evidence_variables)

                second_term = self._enumerate_all(bayes_net, rest(unprocessed_variables), evidence_variables)

                return prob_var_true_given_parents * second_term
            else:
                evars_clone = dict(evidence_variables)

                evars_clone[var] = True
                prob_var_true_given_parents = bayes_net.probability_of(var, True, evars_clone)
                second_term = self._enumerate_all(bayes_net, rest(unprocessed_variables), evars_clone)

                true_probability_var = prob_var_true_given_parents * second_term

                evars_clone[var] = False
                prob_var_false_given_parents = bayes_net.probability_of(var, False, evars_clone)
                second_term = self._enumerate_all(bayes_net, rest(unprocessed_variables), evars_clone)

                false_probability_var = prob_var_false_given_parents * second_term

                return true_probability_var + false_probability_var
