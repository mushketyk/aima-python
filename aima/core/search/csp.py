from abc import ABCMeta

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

class Variable:
    """
    Variable is an object with unique name.
    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "CSPVariable('" + str(self.name) + "')"

    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False

        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Domain:
    """
    Defines set of values that can be assigned to a variable
    """
    def __init__(self, values):
        """

        :param values: values that can be assigned
        :return:
        """
        self.values = []

        for value in values:
            self.values.append(value)

    def size(self):
        """
        Get number of values in domain

        :return (int): number of values
        """
        return len(self.values)

    def get(self, index):
        """
        Get value with specified number

        :param index: number of value in domain
        :return: value from the domain
        """

        return self.values[index]

    def remove(self, value):
        """
        Remove value from domain

        :param value: value to remove
        :return: None
        """
        self.values.remove(value)

    def is_empty(self):
        """
        Check if domain is empty

        :return (bool): True if domain is empty, False otherwise
        """
        return len(self.values) == 0

    def contains(self, value):
        """
        Check if specified value belongs to a domain

        :param value: value to check
        :return (bool): True if value belongs to a domain, False otherwise
        """
        return value in self.values

    def __iter__(self):
        return iter(self.values)

    def __eq__(self, other):
        if not isinstance(other, Domain):
            return False

        if self.size() != other.size():
            return False

        for i in range(self.size()):
            if self.get(i) != other.get(i):
                return False

        return True

    def __str__(self):
        return str(self.values)


class Assignment:
    """
    This class holds what values was assigned to what variables
    """
    def __init__(self):
        self.variable_to_value = {}

    def get_variables(self):
        """
        Get assigned variables

        :return list(Variable): list of assigned variables
        """
        return self.variable_to_value.keys()

    def get_assignment(self, var):
        """
        Get value that was assigned to the specified variable

        :param var (Variable):
        :return: assigned value if any was assigned to a specified variable, None otherwise
        """
        return self.variable_to_value.get(var)

    def set_assignment(self, var, value):
        """
        Assign valut to a variable

        :param var: variable to assign
        :param value: value to assign
        :return: None
        """
        self.variable_to_value[var] = value

    def remove_assignment(self, var):
        """
        Remove assignment for a specified variable

        :param var (Variable): variable to remove assignment for
        :return: None
        """

        del self.variable_to_value[var]

    def has_assignment_for(self, var):
        """
        Check if any value was assigned to a specified variable

        :param var (Variable): variable to check
        :return: True if some value was assigned, false otherwise
        """
        return self.variable_to_value.get(var) != None

    def is_consistent(self, constraints):
        """
        Check if current assignment doesn't violate any constraint

        :param constraints (Constraint): constraints to check
        :return (bool): True all constrainsts are satisfied, False otherwise 
        """
        for constraint in constraints:
            if not constraint.is_satisfied_with(self):
                return False
        return True

    def is_complete(self, variables):
        """
        Check if all values were assigned to all variables.

        :param variables iterable(Variables): variables to check
        :return (bool): True if values were assigned to all variables, False otherwise
        """
        for var in variables:
            if not self.has_assignment_for(var):
                return False

        return True

    def is_solution(self, csp):
        """
        Check if current assignment is a solution to the specifed CSP problem

        :param csp (CSP):
        :return (bool): True is current assignment is a solution, False otherwise.
        """
        return self.is_consistent(csp.get_constraints()) and self.is_complete(csp.get_variables())

    def copy(self):
        copy = Assignment()
        copy.variable_to_value = self.variable_to_value.copy()

        return copy

    def __str__(self):
        first = True
        result = "{"
        for var in self.variable_to_value.keys():
            if not first:
                result += ", "
            result += str(var) + " = " + str(self.variable_to_value[var])
            first = False

        result += "}"
        return result


class Constraint(metaclass=ABCMeta):
    """
    Abstract class for specifying a constraint in CSP problem
    """
    def get_scope(self):
        """
        Get variables that are constrained by an instance of this class

        :return iterable(Variable):
        """
        raise NotImplementedError()

    def is_satisfied_with(self, assignment):
        raise NotImplementedError()

class NotEqualConstraint(Constraint):
    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2
        self.scope = (var1, var2)

    def get_scope(self):
        return self.scope

    def is_satisfied_with(self, assignment):
        value1 = assignment.get_assignment(self.var1)

        return value1 == None or (not value1 == assignment.get_assignment(self.var2))


class CSP:

    def __init__(self, variables):
        self.variables = list(variables)
        self.domains = {}
        self.constraints = []
        self.var_constraints = {}

        for variable in variables:
            self.domains[variable] = []
            self.var_constraints[variable] = []

    def get_variables(self):
        return self.variables

    def get_domain(self, var):
        return self.domains[var]

    def set_domain(self, var, domain):
        self.domains[var] = domain

    def remove_value_from_domain(self, var, value):
        self.domains[var].remove(value)

    def get_constraints(self, var=None):
        if var != None:
            return self.var_constraints[var]
        else:
            return self.constraints

    def add_constraint(self, constraint):
        self.constraints.append(constraint)
        for var in constraint.get_scope():
            self.var_constraints[var].append(constraint)

    def get_neighbor(self, var, constraint):
        pass

    def copy_domains(self):
        result = CSP()
        result.constraints = list(self.constraints)
        result.var_constraints = self.var_constraints.copy()
        result.domains = self.domains.copy()
        

class CSPStateListener(metaclass=ABCMeta):
    def state_changed(self, csp, assignment):
        raise NotImplementedError()


class SolutionStrategy:
    def __init__(self):
        self.listeners = []

    def add_csp_state_listener(self, listener):
        self.listeners.append(listener)

    def remove_csp_state_listener(self, listener):
        self.listeners.remove(listener)

    def _notify_state_changed(self, csp, assignment=None):
        for listener in self.listeners:
            listener.state_changed(csp, assignment)

    def solve(self, csp):
        raise NotImplementedError()

    
# Artificial Intelligence A Modern Approach (3rd Ed.): Figure 6.5, Page 215.
# 
#
# function BACKTRACKING-SEARCH(csp) returns a solution, or failure
#    return BACKTRACK({ }, csp)
# 
# function BACKTRACK(assignment, csp) returns a solution, or failure
#    if assignment is complete then return assignment
#    var = SELECT-UNASSIGNED-VARIABLE(csp)
#    for each value in ORDER-DOMAIN-VALUES(var, assignment, csp) do
#       if value is consistent with assignment then
#         add {var = value} to assignment
#         inferences = INFERENCE(csp, var, value)
#         if inferences != failure then
#             add inferences to assignment
#             result = BACKTRACK(assignment, csp)
#             if result != failure then
#                return result
#         remove {var = value} and inferences from assignment
#    return failure
# 
# Figure 6.5 A simple backtracking algorithm for constraint satisfaction
# problems. The algorithm is modeled on the recursive depth-first search of
# Chapter 3. By varying the functions SELECT-UNASSIGNED-VARIABLE and
# ORDER-DOMAIN-VALUES, we can implement the general-purpose heuristic discussed
# in the text. The function INFERENCE can optionally be used to impose arc-,
# path-, or k-consistency, as desired. If a value choice leads to failure
# (noticed wither by INFERENCE or by BACKTRACK), then value assignments
# (including those made by INFERENCE) are removed from the current assignment
# and a new value is tried.
class BacktrackingStrategy(SolutionStrategy):
    # function BACKTRACKING-SEARCH(csp) returns a solution, or failure
    # return BACKTRACK({ }, csp)
    def solve(self, csp):
        return self._recursive_backtrack_search(csp, Assignment())

    # function BACKTRACK(assignment, csp) returns a solution, or failure
    def _recursive_backtrack_search(self, csp, assignment):
        result = None
        # if assignment is complete then return assignment
        if assignment.is_complete(csp.get_variables()):
            result = assignment
        else:
            # var = SELECT-UNASSIGNED-VARIABLE(csp)
            var = self._select_unassigned_variable(assignment, csp)
            # for each value in ORDER-DOMAIN-VALUES(var, assignment, csp) do
            for value in self._order_domain_values(var, csp):
                # add {var = value} to assignment
                assignment.set_assignment(var, value)
                # inferences = INFERENCE(csp, var, value)
                # if inferences != failure then
                if assignment.is_consistent(csp.get_constraints(var)):
                    # result = BACKTRACK(assignment, csp)
                    result = self._recursive_backtrack_search(csp, assignment)
                    # if result != failure then
                    if result != None:
                        # return result
                        break
                # remove {var = value} and inferences from assignment
                assignment.remove_assignment(var)

        return result

    def _select_unassigned_variable(self, assignment, csp):
        for var in csp.get_variables():
            if not assignment.has_assignment_for(var):
                return var

        return None

    def _order_domain_values(self, var, csp):
        return csp.get_domain(var)


class AC3Strategy(SolutionStrategy):
    pass

class MinConflictsStrategy(SolutionStrategy):
    pass

class MapCSP(CSP):
    NSW = Variable("NSW")
    NT = Variable("NT")
    Q = Variable("Q")
    SA = Variable("SA")
    T = Variable("T")
    V = Variable("V")
    WA = Variable("WA")
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"

    def __init__(self):
        super().__init__(self._collect_variables())
        colors = Domain((self.RED, self.GREEN, self.BLUE))

        for var in self.get_variables():
            self.set_domain(var, colors)

        self.add_constraint(NotEqualConstraint(self.WA, self.NT))
        self.add_constraint(NotEqualConstraint(self.WA, self.SA))
        self.add_constraint(NotEqualConstraint(self.NT, self.SA))
        self.add_constraint(NotEqualConstraint(self.NT, self.Q))
        self.add_constraint(NotEqualConstraint(self.SA, self.Q))
        self.add_constraint(NotEqualConstraint(self.SA, self.NSW))
        self.add_constraint(NotEqualConstraint(self.SA, self.V))
        self.add_constraint(NotEqualConstraint(self.Q, self.NSW))
        self.add_constraint(NotEqualConstraint(self.NSW, self.V))

    def _collect_variables(self):
        variables = []
        variables.append(self.NSW)
        variables.append(self.NT)
        variables.append(self.Q)
        variables.append(self.SA)
        variables.append(self.T)
        variables.append(self.V)
        variables.append(self.WA)

        return variables
