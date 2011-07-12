from aima.core.logic.common import *

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'


class PropositionalLogicLexer(Lexer):

    def __init__(self, input):
        super().__init__(input)
        self.tokens = {"NOT" : NotToken, "AND" : AndToken, "OR" : OrToken, "TRUE" : TrueToken, "FALSE" : FalseToken}

    def get_next_token(self):
        self._skip_whitespaces()

        symbol = self._get_next_symbol()

        if symbol == None:
            return EOLToken()
        if symbol == '<':
            return self._biconditional_symbol()
        elif symbol == '=':
            return self._implication_symbol()
        elif symbol == '(':
            return LeftParToken()
        elif symbol == ')':
            return RightParToken()
        elif symbol.isidentifier():
            self._back()
            return self._identifier()
        else:
            raise LexerError("Unexpected symbol " + symbol)
        
    def _biconditional_symbol(self):
        """
        Read symbol '<=>' from input stream.

        :return: BiconditionalToken if input string contains biconditional token
        """
        # First symbol was read in get_next_token()
        self._expect('=')
        self._expect('>')

        return BiconditionalToken()

    def _implication_symbol(self):
        """
        Read implication symbol from string

        :return: ImplicationToken if string contains biconditional token
        """
        self._expect('>')

        return ImplicationToken()

    def _identifier(self):
        """
        Read identifier from a string

        :return: read identifier
        """
        identifier = ""
        while True:
            symbol = self._get_next_symbol()
            if symbol != None and symbol.isidentifier():
                identifier += symbol
            else:
                if symbol != None:
                    self._back()
                break

        return self._create_identifier_token(identifier)

    def _create_identifier_token(self, identifier):
        special_id_constructor = self.tokens.get(identifier)
        if special_id_constructor:
            # Create token for special identifier
            return special_id_constructor()
        else:
            return IdentifierToken(identifier)





