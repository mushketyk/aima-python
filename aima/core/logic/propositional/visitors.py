from aima.core.logic.common import TermVisitor, TokenTypes

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

        return self.calculation_result[root_term]

    def visit_false_term(self, term):
        self.calculation_result[term] = False

    def visit_true_term(self, term):
        self.calculation_result[term] = True

    def visit_symbol_term(self, term):
        self.calculation_result[term] = self.symbols_table[term.name]

    def visit_function_term(self, term):
        if term.type == TokenTypes.NOT:
            self.calculation_result[term] = not self.calculation_result[term.children[0]]
        elif term.type == TokenTypes.AND:
            v1 = self.calculation_result[term.children[0]]
            v2 = self.calculation_result[term.children[1]]

            self.calculation_result[term] = v1 and v2
        elif term.type == TokenTypes.OR:
            v1 = self.calculation_result[term.children[0]]
            v2 = self.calculation_result[term.children[1]]

            self.calculation_result[term] = v1 or v2

        elif term.type == TokenTypes.IMPLICATION:
            v1 = self.calculation_result[term.children[0]]
            v2 = self.calculation_result[term.children[1]]

            self.calculation_result[term] =  (not v1) or v2

        elif term.type == TokenTypes.BICONDITIONAL:
            v1 = self.calculation_result[term.children[0]]
            v2 = self.calculation_result[term.children[1]]

            self.calculation_result[term] =  ((not v1) or v2) and ((not v2) or v1)

        

    
        