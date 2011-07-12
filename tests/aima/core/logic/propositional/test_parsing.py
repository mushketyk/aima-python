from aima.core.logic.common import IdentifierToken, EOLToken, NotToken, TrueToken, AndToken, FalseToken, BiconditionalToken, ImplicationToken, LeftParToken, OrToken, RightParToken
from aima.core.logic.propositional.parsing import PropositionalLogicLexer

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

    def _test_lexer(self, input, expected_tokens):
        ppl = PropositionalLogicLexer(input)

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
        ppl = PropositionalLogicLexer("Hello AND lexer")
        self.assertEquals(IdentifierToken("Hello"), ppl.get_next_token())
        ppl.mark()

        self.assertEquals(AndToken(), ppl.get_next_token())
        self.assertEquals(IdentifierToken("lexer"), ppl.get_next_token())

        ppl.rollback()
        self.assertEquals(AndToken(), ppl.get_next_token())
        self.assertEquals(IdentifierToken("lexer"), ppl.get_next_token())
        self.assertEquals(EOLToken(), ppl.get_next_token())


if __name__ == '__main__':
    unittest.main()
