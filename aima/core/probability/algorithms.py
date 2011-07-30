from aima.core.util.functions import normalize

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


    def __init__(self, *variables):
        """
        :param variables iterable(str): names of all variables in this probability distribution
        """
        self.rows = []
        self.variables_places = {}

        i = 0
        for var in variables:
            self.variables_places[var] = i
            i += 1

    def set(self, probability, *values):
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

                if not row.matches(self.variables_places[var_name], cond_value):
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