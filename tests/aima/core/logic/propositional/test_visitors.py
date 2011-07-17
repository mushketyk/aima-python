from aima.core.logic.common import Parser, SymbolTerm, AndTerm, OrTerm, NotTerm
from aima.core.logic.propositional.parsing import PLParser, PLLexer
from aima.core.logic.propositional.visitors import SymbolsCollector, Model, CNFTransformer, CNFClauseGatherer, CNFOrGatherer

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

    def test_root_and_term(self):
        self._test_transformer("((A => B) AND C)", AndTerm(OrTerm(NotTerm(SymbolTerm("A")),
                                                                  SymbolTerm("B")),
                                                           SymbolTerm("C")))

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

class CNFClauseGathererTest(unittest.TestCase):
    def test_symbol(self):
        self._test_gatherer_str("A", [SymbolTerm("A")])

    def test_not_sentence(self):
        self._test_gatherer_str("NOT A", [NotTerm(SymbolTerm("A"))])

    def test_simple_and_clause(self):
        self._test_gatherer_str("A AND B", [SymbolTerm("A"), SymbolTerm("B")])

    def test_simple_and_multi_clause(self):
        self._test_gatherer_str("(A AND B) AND C", [SymbolTerm("A"), SymbolTerm("B"), SymbolTerm("C")])

    def test_simple_and_multi_clause2(self):
        self._test_gatherer_str("D AND (A AND B) AND C", [SymbolTerm("A"), SymbolTerm("B"), SymbolTerm("C"), SymbolTerm("D")])

    def test_aima_example(self):
        parser = PLParser()
        sentence = parser.parse("B11 <=> (P12 OR P21)")

        transformer = CNFTransformer()
        cnf = transformer.transform(sentence)

        self._test_gatherer(cnf, [OrTerm(NotTerm(SymbolTerm("B11")),
                                                   OrTerm(SymbolTerm("P12"),
                                                          SymbolTerm("P21"))),
                                    OrTerm(NotTerm(SymbolTerm("P12")),
                                                   SymbolTerm("B11")),
                                    OrTerm(NotTerm(SymbolTerm("P21")),
                                                   SymbolTerm("B11"))])


    def _test_gatherer_str(self, expression, expected_clauses):
        parser = PLParser()
        sentence = parser.parse(expression)

        self._test_gatherer(sentence, expected_clauses)

    def _test_gatherer(self, sentence, expected_clauses):
        ccg = CNFClauseGatherer()
        result = ccg.collect(sentence)

        self.assertSetEqual(set(expected_clauses), set(result))

class CNFOrGathererTest(unittest.TestCase):
    def test_single_symbol(self):
        self._test_gatherer("A", {SymbolTerm("A")})

    def test_one_or(self):
        self._test_gatherer("A OR B", {SymbolTerm("A"), SymbolTerm("B")})

    def test_two_ors(self):
        self._test_gatherer("A OR B OR C", {SymbolTerm("A"), SymbolTerm("B"), SymbolTerm("C")})

    def test_four_ors(self):
        self._test_gatherer("A OR B OR C OR D", {SymbolTerm("A"), SymbolTerm("B"), SymbolTerm("C"), SymbolTerm("D")})

    def test_one_not(self):
        self._test_gatherer("NOT A", set(), {SymbolTerm("A")})

    def test_or_and_not(self):
        self._test_gatherer("A OR (NOT B)", {SymbolTerm("A")}, {SymbolTerm("B")})

    def test_or_and_not2(self):
        self._test_gatherer("(NOT A) OR (NOT B) OR C", {SymbolTerm("C")}, {SymbolTerm("A"), SymbolTerm("B")})

    def _test_gatherer(self, expression, expected_symbols, expected_not_symbols=set()):
        sentence = PLParser().parse(expression)

        (symbols, not_symbols) = CNFOrGatherer().collect(sentence)

        self.assertSetEqual(expected_symbols, symbols)
        self.assertSetEqual(not_symbols, expected_not_symbols)


if __name__ == '__main__':
    unittest.main()
