from aima.core.logic.common import *

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'


class PLLexer(Lexer):
    """
    Lexical analyser for propositional logic
    """
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
        elif symbol.isalpha():
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
        identifier = self._get_next_symbol()

        while True:
            symbol = self._get_next_symbol()
            if symbol != None and symbol.isalnum():
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


class PLParser(Parser):
    """
    Parser for propositional logical
    """
    def __init__(self):
        super().__init__()
        self._operator_ctors = {TokenTypes.AND : AndTerm, TokenTypes.OR : OrTerm, TokenTypes.BICONDITIONAL : BiconditionalTerm,
                                TokenTypes.IMPLICATION : ImplicationTerm}

    def _implementation_specific_parsing(self):
        return self._parse_sentence()

    def _parse_sentence(self):
        token = self._get_token()

        sentence = None
        if token.type == TokenTypes.LEFT_PAR:
            sentence = self._parse_sentence()
            self._match(TokenTypes.RIGHT_PAR)

        elif token.type == TokenTypes.NOT:
            sentence = self._parse_not_sentence()
        elif token.type == TokenTypes.FALSE:
            sentence = FalseTerm()
        elif token.type == TokenTypes.TRUE:
            sentence = TrueTerm()
        elif token.type == TokenTypes.IDENTIFIER:
            sentence = SymbolTerm(token.str)
        else:
            raise ParserError("Unexpected token")

        self.lexer.mark()
        token = self._get_token()

        if self._is_operator(token.type):
            sentence2 = self._parse_sentence()
            operator_ctor = self._operator_ctors[token.type]
            return operator_ctor(sentence, sentence2)
        else:
            self.lexer.rollback()
            return sentence
        

    def _parse_not_sentence(self):
        sentence = self._parse_sentence()
        return NotTerm(sentence)

    def _is_operator(self, type):
        return type in {TokenTypes.OR, TokenTypes.AND, TokenTypes.BICONDITIONAL, TokenTypes.IMPLICATION}










