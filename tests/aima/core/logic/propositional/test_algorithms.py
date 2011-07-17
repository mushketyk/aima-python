from aima.core.logic.common import AndTerm, SymbolTerm, BiconditionalTerm, ImplicationTerm, NotTerm, OrTerm
from aima.core.logic.propositional.algorithms import KnowledgeBase, TTEntails, PLResolution, EmptyClause, PLFCEntails, DPLL
from aima.core.logic.propositional.parsing import PLParser
from aima.core.logic.propositional.visitors import CNFClauseGatherer, Model

__author__ = 'proger'

import unittest

class KnowledgeBaseTest(unittest.TestCase):
    def test_as_sentence(self):
        kb = KnowledgeBase()

        kb.tell_str("A")
        kb.tell_str("A OR B")
        kb.tell_str("C <=> D")
        kb.tell_str("E => NOT F")

        sentence = kb.as_sentence()
        expected_sentence = AndTerm(SymbolTerm("A"),
                                    AndTerm(OrTerm(SymbolTerm("A"),
                                                   SymbolTerm("B")),
                                           AndTerm(BiconditionalTerm(SymbolTerm("C"),
                                                                     SymbolTerm("D")),
                                                   ImplicationTerm(SymbolTerm("E"),
                                                                   NotTerm(SymbolTerm("F")))))
                                   )

        self.assertEqual(expected_sentence, sentence)

class TTEntailsTest(unittest.TestCase):
    def test_simple_sentence1(self):
        kb = KnowledgeBase()
        kb.tell_str("A AND B")
        tte = TTEntails()

        result = tte.tt_entails(kb, "A")
        self.assertTrue(result)

    def test_simple_sentence2(self):
        kb = KnowledgeBase()
        kb.tell_str("A OR B")
        tte = TTEntails()

        result = tte.tt_entails(kb, "A")
        self.assertFalse(result)

    def test_simple_sentence3(self):
        kb = KnowledgeBase()
        kb.tell_str("(A => B) AND A")
        tte = TTEntails()

        result = tte.tt_entails(kb, "B")
        self.assertTrue(result)

    def test_simple_sentence4(self):
        kb = KnowledgeBase()
        kb.tell_str("(A => B) AND B")
        tte = TTEntails()

        result = tte.tt_entails(kb, "A")
        self.assertFalse(result)

    def test_simple_sentence5(self):
        kb = KnowledgeBase()
        kb.tell_str("A")
        tte = TTEntails()

        result = tte.tt_entails(kb, "NOT A")
        self.assertFalse(result)

    def test_simple_sentence6(self):
        kb = KnowledgeBase()
        kb.tell_str("NOT A")
        tte = TTEntails()

        result = tte.tt_entails(kb, "A")
        self.assertFalse(result)

    def test_unknown_symbol(self):
        kb = KnowledgeBase()
        kb.tell_str("(A => B) AND B")
        tte = TTEntails()

        result = tte.tt_entails(kb, "X")
        self.assertFalse(result)

    def test_aima_example(self):
        kb = KnowledgeBase()
        kb.tell_str("(NOT P11)")
        kb.tell_str("(B11 <=> (P12 OR P21))")
        kb.tell_str("(B21 <=> ((P11 OR P22) OR P31))")
        kb.tell_str("(NOT B11)")
        kb.tell_str("(B21)")

        tte = TTEntails()

        self.assertTrue(tte.tt_entails(kb, "NOT P12"))
        self.assertFalse((tte.tt_entails(kb, "P22")))

class PLResolutionTest(unittest.TestCase):
    def test_pl_resolve_with_one_literal(self):
        self._test_pl_resolve("A OR B", "(NOT B) OR C", OrTerm(SymbolTerm("A"),
                                                               SymbolTerm("C")))

    def test_pl_resolve_with_different_symbols(self):
        self._test_pl_resolve("NOT C", "C", EmptyClause())

    def test_pl_resolve1(self):
        self._test_resolution("(B11 => (NOT P11)) AND B11", "P11", False)

    def test_pl_resolve2(self):
        self._test_resolution("(A AND B)", "B", True)

    def test_pl_resolve3(self):
        self._test_resolution("(B11 => (NOT P11)) AND B11", "NOT P11", True)

    def test_pl_resolve4(self):
        self._test_resolution("(A OR B)", "B", False)

    def test_pl_resolve5(self):
        self._test_resolution("((B11 =>  (NOT P11)) AND B11)", "(NOT B11)", False)

    def _test_resolution(self, expression, question, expected_result):
        kb = KnowledgeBase()
        kb.tell_str(expression)
        question_term = PLParser().parse(question)

        pl_resolution = PLResolution()
        result = pl_resolution.pl_resolution(kb, question_term)
        self.assertEquals(expected_result, result)

    def _test_pl_resolve(self, expr1, expr2, expected_symbol):
        sentence1 = PLParser().parse(expr1)
        sentence2 = PLParser().parse(expr2)

        pl_resolution = PLResolution()

        symbol = pl_resolution._pl_resolve(sentence1, sentence2)
        self.assertEquals(expected_symbol, symbol)

class PLFCEntailsTest(unittest.TestCase):
    def test_single_symbol(self):
        self._test_plfc_entails(["A => B", "A"], "B", True)

    def test_cyclic_expression(self):
        self._test_plfc_entails(["A => B", "B => A", "A"], "C", False)

    def test_and_example(self):
        self._test_plfc_entails(["(A AND B) => C", "A", "B"], "C", True)

    def test_aima_example(self):
        self._test_plfc_entails(["A", "B", "(A AND B) => L", "(A AND P) => L", "(B AND L) => M", "(L AND M) => P", "P => Q"],
                                "Q", True)

    def _test_plfc_entails(self, expressions, question, expected_result):
        kb = KnowledgeBase()
        kb.tell_all_str(expressions)

        question_sentence = PLParser().parse(question)
        plfc_entails = PLFCEntails()
        result = plfc_entails.plfc_entails(kb, question_sentence)

        self.assertEquals(expected_result, result)

class DPLLTest(unittest.TestCase):
    def test_dpll_when_all_clauses_true(self):
        model = Model()
        model = model.extend("A", True).extend("B", True)

        sentence = PLParser().parse("(A OR B) AND (A OR B)")
        result = DPLL().dpll_satisfiable(sentence, model)
        self.assertTrue(result)

    def test_dpll_return_false_with_one_false_in_model(self):
        model = Model().extend("A", True).extend("B", False)

        sentence = PLParser().parse("(A OR B) AND (A => B)")
        result = DPLL().dpll_satisfiable(sentence, model)
        self.assertFalse(result)

    def test_dpll_succeeds_with_a_and_not_a(self):
        sentence = PLParser().parse("A AND (NOT A)")
        result = DPLL().dpll_satisfiable(sentence)
        self.assertFalse(result)

    def test_dpll1(self):
        kb = KnowledgeBase()
        kb.tell_str("(B12 <=> (P11 OR (P13 OR (P22 OR P02))))")
        kb.tell_str("(B21 <=> (P20 OR (P22 OR (P31 OR P11))))")
        kb.tell_str("(B01 <=> (P00 OR (P02 OR P11)))")
        kb.tell_str("(B10 <=> (P11 OR (P20 OR P00)))")
        kb.tell_str("(NOT B21)")
        kb.tell_str("(NOT B12)")
        kb.tell_str("(B10)")
        kb.tell_str("(B01)")

        kb.ask_with_dpll(SymbolTerm("P00"))
        kb.ask_with_dpll(NotTerm(SymbolTerm("P00")))

if __name__ == '__main__':
    unittest.main()
