from aima.core.logic.common import TermVisitor, TokenTypes, ImplicationTerm, AndTerm, NotTerm, OrTerm

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

class SymbolsCollector(TermVisitor):
    def __init__(self):
        self.symbols = set()

    def clear(self):
        self.symbols = set()

    def collect_symbols(self, root_term):
        self.clear()
        root_term.accept_visitor(self)

        return self.symbols

    def visit_symbol_term(self, term):
        self.symbols.add(term.name)


class Model(TermVisitor):
    def __init__(self):
        self.calculation_result = {}
        self.symbols_table = {}

    def clear(self):
        self.calculation_result = {}
        self.symbols_table = {}

    def extend(self, symbol, value):
        m = Model()
        m.symbols_table = self.symbols_table.copy()
        m.symbols_table[symbol] = value

        return m

    def is_true(self, root_term):
        self.calculation_result = {}
        root_term.accept_visitor(self)

        return self.calculation_result.get(root_term) == True

    def visit_false_term(self, term):
        self.calculation_result[term] = False

    def visit_true_term(self, term):
        self.calculation_result[term] = True

    def visit_symbol_term(self, term):
        self.calculation_result[term] = self.symbols_table.get(term.name)

    def visit_function_term(self, term):
        v1 = self.calculation_result[term.children[0]]
        if v1 == None:
            self.calculation_result[term] = None
        elif term.type == TokenTypes.NOT:
            self.calculation_result[term] = not self.calculation_result[term.children[0]]
        else:

            v2 = self.calculation_result[term.children[1]]
            if v2 == None:
                self.calculation_result[term] = None
            if term.type == TokenTypes.AND:
                self.calculation_result[term] = v1 and v2

            elif term.type == TokenTypes.OR:
                self.calculation_result[term] = v1 or v2

            elif term.type == TokenTypes.IMPLICATION:
                self.calculation_result[term] =  (not v1) or v2

            elif term.type == TokenTypes.BICONDITIONAL:
                self.calculation_result[term] =  ((not v1) or v2) and ((not v2) or v1)

    def get_assigned_symbols(self):
        return self.symbols_table.keys()

    def flip(self, symbol):
        self.symbols_table[symbol] = not self.symbols_table[symbol]

    def __str__(self):
        return "Model: " + str(self.symbols_table)

class CNFTransformer:
    """
    Transformer that transformer any expression in propositional logic into CNF expression
    """
    def transform(self, root_term):
        """
        Transform expression presented by root term

        :param root_term (Term): root term of the expression
        :return (Term): root term of transformed expression
        """
        return self._transform_term(root_term)

    def _transform_term(self, term):
        if term.type == TokenTypes.NOT:
            return self._transform_not_expression(term)
        elif term.type == TokenTypes.BICONDITIONAL:
            return self._transform_biconditional_expression(term)
        elif term.type == TokenTypes.IMPLICATION:
            return self._transform_implication(term)
        elif term.type == TokenTypes.OR:
            return self._transform_or(term)
        elif term.type == TokenTypes.AND:
            return AndTerm(self._transform_term(term.children[0]),
                           self._transform_term(term.children[1]))
        else:
            return term

    def _transform_not_expression(self, term):
        not_child = term.children[0]
        # Check if we can remove double NOT
        if not_child.type == TokenTypes.NOT:
            return self.transform(not_child.children[0])
        # De Morgan rule NOT (A OR B) == (NOT A) AND (NOT B)
        elif not_child.type == TokenTypes.OR:
            return AndTerm(self.transform(NotTerm(not_child.children[0])),
                           self.transform(NotTerm(not_child.children[1])))
        # De Morgan rule NOT (A AND B) == (NOT A) OR (NOT B)
        elif not_child.type == TokenTypes.AND:
            return self.transform(OrTerm(self.transform(NotTerm(not_child.children[0])),
                                         self.transform(NotTerm(not_child.children[1]))))

        # No rules, just return NOT expression
        return term

    def _transform_or(self, term):
        left_child = term.children[0]
        right_child = term.children[1]

        # If we have A OR (B AND C)
        if not left_child.is_function() and right_child.type == TokenTypes.AND:
            and_expression = right_child
            symbol = left_child
        # If we have (B AND C) OR A
        elif not right_child.is_function() and left_child.type == TokenTypes.AND:
            and_expression = left_child
            symbol = right_child
        else:
            # Just return OR term
            return term

        and_left_child = and_expression.children[0]
        and_right_child = and_expression.children[1]

        # OR distribution; A OR (B AND C) == (A OR B) AND (A OR C)
        return AndTerm(self.transform(OrTerm(and_left_child, symbol)),
                       self.transform(OrTerm(and_right_child, symbol)))


    def _transform_implication(self, term):
        first_child = NotTerm(term.children[0])
        second_child = term.children[1]

        # Implication transformation; A => B == (NOT A) OR B
        return self.transform(OrTerm(self.transform(first_child), second_child))

    def _transform_biconditional_expression(self, term):
        first_implication = ImplicationTerm(self.transform(term.children[0]),
                                            self.transform(term.children[1]))

        second_implication = ImplicationTerm(self.transform(term.children[1]),
                                             self.transform(term.children[0]))

        # Biconditional term transformation; A <=> B == (A => B) AND (B => A)
        return AndTerm(self.transform(first_implication), self.transform(second_implication))


class CNFClauseGatherer(TermVisitor):
    """
    Select set of expressions separated by AND in CNF
    """
    def __init__(self):
        self.clauses = set()

    def collect(self, root_term):
        # If we have expressions like A OR B, D, NOT C; just return the root term
        if root_term.type != TokenTypes.AND:
            return {root_term}
        else:
            self.clauses = set()
            root_term.accept_visitor(self)

            return self.clauses

    def visit_function_term(self, term):
        if term.type == TokenTypes.AND:
            left_child = term.children[0]
            right_child = term.children[1]

            if left_child.type != TokenTypes.AND:
                self.clauses.add(left_child)
            if right_child.type != TokenTypes.AND:
                self.clauses.add(right_child)

class CNFOrGatherer(TermVisitor):
    """
    Gather all symbols in CNF clause.
    """
    def __init__(self):
        self.symbols = set()
        self.not_symbols = set()

    def collect(self, root_term):
        """
        Collect all symbols in CNF clause. If we have A OR B OR NOT C, this will return {A, B}, {C}.

        :param root_term: root term of the CNF clause
        :return set(Term), set(Term): pair of set of terms, where fist element of pair is symbols without NOT, and second
        set is a set of inverted symbols
        """
        if root_term.type == TokenTypes.IDENTIFIER:
            return {root_term}, set()

        self.symbols = set()
        self.not_symbols = set()

        root_term.accept_visitor(self)

        return self.symbols, self.not_symbols

    def visit_function_term(self, term):
        if term.type == TokenTypes.OR:
            left_child = term.children[0]
            right_child = term.children[1]

            self._add_child(left_child)
            self._add_child(right_child)
        elif term.type == TokenTypes.NOT:
            self._add_child(term)

    def _add_child(self, term):
        if term.type == TokenTypes.NOT:
            self.not_symbols.add(term.children[0])
        elif term.type == TokenTypes.IDENTIFIER:
            self.symbols.add(term)



        

    
        