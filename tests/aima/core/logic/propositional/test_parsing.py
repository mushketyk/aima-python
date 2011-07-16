from aima.core.logic.common import IdentifierToken, EOLToken, NotToken, TrueToken, AndToken, FalseToken, BiconditionalToken, ImplicationToken, LeftParToken, OrToken, RightParToken, NotTerm, SymbolTerm, AndTerm, ImplicationTerm
from aima.core.logic.propositional.parsing import PLLexer, PLParser

__author__ = 'Ivan Mushketik'

import unittest

class LexerTest(unittest.TestCase):
    def test_ids(self):
        self._test_lexer("Hello lexer",
            [IdentifierToken("Hello"), IdentifierToken("lexer"), EOLToken()])

    def test_empty_line(self):
        self._test_lexer("",
            [EOLToken()])

    def test_different_tokens(self):
        self._test_lexer("NOT TRUE AND FALSE <=> Me => (You OR They)",
            [NotToken(), TrueToken(), AndToken(), FalseToken(), BiconditionalToken(), IdentifierToken("Me"), ImplicationToken(),
             LeftParToken(), IdentifierToken("You"), OrToken(), IdentifierToken("They"), RightParToken(), EOLToken()])

    def test_alphanum_identifier(self):
        self._test_lexer("NOT P11",
            [NotToken(), IdentifierToken("P11"), EOLToken()])

    def _test_lexer(self, input, expected_tokens):
        ppl = PLLexer(input)

        tokens = self._get_tokens(ppl)
        self.assertSequenceEqual(expected_tokens, tokens)

    def _get_tokens(self, ppl):
        tokens = []
        while True:
            token = ppl.get_next_token()
            tokens.append(token)
            if token == EOLToken():
                break
        return tokens

    def test_marking(self):
        ppl = PLLexer("Hello AND lexer")
        self.assertEquals(IdentifierToken("Hello"), ppl.get_next_token())
        ppl.mark()

        self.assertEquals(AndToken(), ppl.get_next_token())
        self.assertEquals(IdentifierToken("lexer"), ppl.get_next_token())

        ppl.rollback()
        self.assertEquals(AndToken(), ppl.get_next_token())
        self.assertEquals(IdentifierToken("lexer"), ppl.get_next_token())
        self.assertEquals(EOLToken(), ppl.get_next_token())


class ParserTest(unittest.TestCase):
    def test_not(self):
        self._test_parser("NOT Java", NotTerm(SymbolTerm("Java")))

    def test_and(self):
                                                       # Here comes my LISP nostalgia
        self._test_parser("Java AND Haskell => Scala", AndTerm(SymbolTerm("Java"),
                                                               ImplicationTerm(SymbolTerm("Haskell"),
                                                                               SymbolTerm("Scala"))))

    def test_parenth(self):
        self._test_parser("(Java AND Haskell) => Scala", ImplicationTerm(AndTerm(SymbolTerm("Java"),
                                                                                 SymbolTerm("Haskell")),
                                                                         SymbolTerm("Scala")))

    def test_complex_not(self):
        self._test_parser("(Java AND NOT C) => Scala", ImplicationTerm(AndTerm(SymbolTerm("Java"),
                                                                                     NotTerm(SymbolTerm("C"))),
                                                                             SymbolTerm("Scala")))

    def test_complex_and(self):
        self._test_parser("(A => B) AND (B => A)", AndTerm(ImplicationTerm(SymbolTerm("A"),
                                                                           SymbolTerm("B")),
                                                           ImplicationTerm(SymbolTerm("B"),
                                                                           SymbolTerm("A"))))

    def test_not_parenth(self):
        self._test_parser("(NOT A)", NotTerm(SymbolTerm("A")))

    def _test_parser(self, str, expected_term):
        parser = PLParser()
        result_term = parser.parse(str)

        self.assertEqual(expected_term, result_term)


if __name__ == '__main__':
    unittest.main()
