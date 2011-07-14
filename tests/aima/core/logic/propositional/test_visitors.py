from aima.core.logic.propositional.parsing import PLParser, PLLexer
from aima.core.logic.propositional.visitors import SymbolsCollector, Model

__author__ = 'proger'

import unittest

class TestSymbolCollector(unittest.TestCase):
    def test_collect_symbols(self):
        expression = "(A AND NOT B) => B <=> NOT C OR D => E"
        parser = PLParser()
        root_term = parser.parse(PLLexer(expression))
        sc = SymbolsCollector()

        sc.collect_symbols(root_term)
        result_symbols = sc.symbols
        expected_symbols = ["A", "B", "C", "D", "E"]

        self.assertSameElements(expected_symbols, result_symbols)

class ModelTest(unittest.TestCase):
    def test_and(self):
        expression = "A AND B"
        parser = PLParser()
        root_term = parser.parse(PLLexer(expression))

        m = Model()
        m = m.extend("A", True).extend("B", True)

        self.assertTrue(m.is_true(root_term))
        m.clear()

        m = m.extend("A", True).extend("B", False)

        self.assertFalse(m.is_true(root_term))
        m.clear()

        m = m.extend("A", False).extend("B", True)

        self.assertFalse(m.is_true(root_term))
        m.clear()

        m = m.extend("A", False).extend("B", False)

        self.assertFalse(m.is_true(root_term))
        m.clear()

    def test_or(self):
        expression = "A OR B"
        parser = PLParser()
        root_term = parser.parse(PLLexer(expression))

        m = Model()
        m = m.extend("A", True).extend("B", True)

        self.assertTrue(m.is_true(root_term))
        m.clear()

        m = m.extend("A", True).extend("B", False)

        self.assertTrue(m.is_true(root_term))
        m.clear()

        m = m.extend("A", False).extend("B", True)

        self.assertTrue(m.is_true(root_term))
        m.clear()

        m = m.extend("A", False).extend("B", False)

        self.assertFalse(m.is_true(root_term))
        m.clear()

    def test_not(self):
        expression = "NOT A"
        parser = PLParser()
        root_term = parser.parse(PLLexer(expression))

        m = Model()
        m = m.extend("A", False)

        self.assertTrue(m.is_true(root_term))
        m.clear()

        m = m.extend("A", True)

        self.assertFalse(m.is_true(root_term))

    def test_biconditional(self):
        expression = "A <=> B"
        parser = PLParser()
        root_term = parser.parse(PLLexer(expression))

        m = Model()
        m = m.extend("A", True).extend("B", True)

        self.assertTrue(m.is_true(root_term))
        m.clear()

        m = m.extend("A", True).extend("B", False)

        self.assertFalse(m.is_true(root_term))
        m.clear()

        m = m.extend("A", False).extend("B", True)

        self.assertFalse(m.is_true(root_term))
        m.clear()

        m = m.extend("A", False).extend("B", False)

        self.assertTrue(m.is_true(root_term))
        m.clear()

    def test_implication(self):
        expression = "A => B"
        parser = PLParser()
        root_term = parser.parse(PLLexer(expression))

        m = Model()
        m = m.extend("A", True).extend("B", True)

        self.assertTrue(m.is_true(root_term))
        m.clear()

        m = m.extend("A", True).extend("B", False)

        self.assertFalse(m.is_true(root_term))
        m.clear()

        m = m.extend("A", False).extend("B", True)

        self.assertTrue(m.is_true(root_term))
        m.clear()

        m = m.extend("A", False).extend("B", False)

        self.assertTrue(m.is_true(root_term))
        m.clear()




if __name__ == '__main__':
    unittest.main()
