from aima.core.logic.common import Parser, SymbolTerm, AndTerm, OrTerm, NotTerm
from aima.core.logic.propositional.parsing import PLParser, PLLexer
from aima.core.logic.propositional.visitors import SymbolsCollector, Model, CNFTransformer

__author__ = 'proger'

import unittest

class TestSymbolCollector(unittest.TestCase):
    def test_collect_symbols(self):
        expression = "(A AND NOT B) => B <=> NOT C OR D => E"
        parser = PLParser()
        root_term = parser.parse(expression)
        sc = SymbolsCollector()

        sc.collect_symbols(root_term)
        result_symbols = sc.symbols
        expected_symbols = ["A", "B", "C", "D", "E"]

        self.assertSameElements(expected_symbols, result_symbols)

class ModelTest(unittest.TestCase):
    def test_and(self):
        expression = "A AND B"
        parser = PLParser()
        root_term = parser.parse(expression)

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
        root_term = parser.parse(expression)

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
        root_term = parser.parse(expression)

        m = Model()
        m = m.extend("A", False)

        self.assertTrue(m.is_true(root_term))
        m.clear()

        m = m.extend("A", True)

        self.assertFalse(m.is_true(root_term))

    def test_biconditional(self):
        expression = "A <=> B"
        parser = PLParser()
        root_term = parser.parse(expression)

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
        root_term = parser.parse(expression)

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

class CNFTransformerTest(unittest.TestCase):
    def test_simple_transform(self):
        self._test_transformer("A", SymbolTerm("A"))

    def test_and(self):
        self._test_transformer("A AND B", AndTerm(SymbolTerm("A"),
                                                  SymbolTerm("B")))

    def test_or(self):
        self._test_transformer("A OR B", OrTerm(SymbolTerm("A"),
                                                SymbolTerm("B")))

    def test_implication_transfromation(self):
        self._test_transformer("A => B", OrTerm(NotTerm(SymbolTerm("A")),
                                                        SymbolTerm("B")))

    def test_biconditional_transformation(self):
        self._test_transformer("A <=> B", AndTerm(OrTerm(NotTerm(SymbolTerm("A")),
                                                                 SymbolTerm("B")),
                                                  OrTerm(NotTerm(SymbolTerm("B")),
                                                                 SymbolTerm("A"))))

    def test_double_negatiation_transformation(self):
        self._test_transformer("NOT (NOT A)", SymbolTerm("A"))

    def test_triple_negatiation_transformation(self):
        self._test_transformer("NOT (NOT (NOT A))", NotTerm(SymbolTerm("A")))

    def test_four_successive_nots_transformation(self):
        self._test_transformer("NOT (NOT (NOT (NOT A)))", SymbolTerm("A"))

    def test_de_morgan1(self):
        self._test_transformer("NOT (A AND B)", OrTerm(NotTerm(SymbolTerm("A")),
                                                       NotTerm(SymbolTerm("B"))))

    def test_de_morgan2(self):
        self._test_transformer("NOT (A OR B)", AndTerm(NotTerm(SymbolTerm("A")),
                                                       NotTerm(SymbolTerm("B"))))

    def test_or_distribution1(self):
        self._test_transformer("(A AND B) OR C", AndTerm(OrTerm(SymbolTerm("A"),
                                                                SymbolTerm("C")),
                                                         OrTerm(SymbolTerm("B"),
                                                                SymbolTerm("C"))))

    def test_or_distribution2(self):
        self._test_transformer("A OR (B AND C)", AndTerm(OrTerm(SymbolTerm("B"),
                                                                SymbolTerm("A")),
                                                         OrTerm(SymbolTerm("C"),
                                                                SymbolTerm("A"))))

    def test_aima_example(self):
        self._test_transformer("B11 <=> (P12 OR P21)", AndTerm(OrTerm(NotTerm(SymbolTerm("B11")),
                                                                      OrTerm(SymbolTerm("P12"),
                                                                             SymbolTerm("P21"))),
                                                               AndTerm(OrTerm(NotTerm(SymbolTerm("P12")),
                                                                              SymbolTerm("B11")),
                                                                       OrTerm(NotTerm(SymbolTerm("P21")),
                                                                              SymbolTerm("B11")))))

    def _test_transformer(self, input, expected_result):
        parser = PLParser()
        sentence = parser.parse(input)

        result = CNFTransformer().transform(sentence)
        self.assertEqual(expected_result, result)

if __name__ == '__main__':
    unittest.main()
