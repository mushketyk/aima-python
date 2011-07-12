__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

class Token:
    def __init__(self, type, str):
        self.type = type
        self.str = str

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False

        return self.str == other.str and self.type == other.type

    def __str__(self):
        return "Token(" + str(self.type) + ", '" + self.str + "')"

class TokenTypes:
    EOL = 0
    BICONDITIONAL = 1
    IMPLICATION = 2
    NOT = 3
    OR = 4
    AND = 5
    LEFT_PAR = 6
    RIGHT_PAR = 7
    TRUE = 8
    FALSE = 9
    IDENTIFIER = 10

class EOLToken(Token):
    def __init__(self):
        super().__init__(TokenTypes.EOL, "")

class BiconditionalToken(Token):
    def __init__(self):
        super().__init__(TokenTypes.BICONDITIONAL, "<=>")

class ImplicationToken(Token):
    def __init__(self):
        super().__init__(TokenTypes.IMPLICATION, "=>")

class NotToken(Token):
    def __init__(self):
        super().__init__(TokenTypes.NOT, "NOT")

class AndToken(Token):
    def __init__(self):
        super().__init__(TokenTypes.AND, "AND")

class OrToken(Token):
    def __init__(self):
        super().__init__(TokenTypes.OR, "OR")

class LeftParToken(Token):
    def __init__(self):
        super().__init__(TokenTypes.LEFT_PAR, "(")

class RightParToken(Token):
    def __init__(self):
        super().__init__(TokenTypes.RIGHT_PAR, ")")

class TrueToken(Token):
    def __init__(self):
        super().__init__(TokenTypes.TRUE, "TRUE")

class FalseToken(Token):
    def __init__(self):
        super().__init__(TokenTypes.FALSE, "FALSE")

class IdentifierToken(Token):
    def __init__(self, name):
        super().__init__(TokenTypes.IDENTIFIER, name)

class Lexer:
    NO_MARK = -1

    def __init__(self, input):
        self.input = input
        self.curr_pos = 0
        self.mark_pos = self.NO_MARK

    def get_next_token(self):
        """
        Get next token.

        :return: next parsed token if any one exists. If end of line found returns EOLToken
        """
        raise NotImplementedError()

    def mark(self):
        """
        Mark current pos in string, so parser could return to it later.

        """
        self.mark_pos = self.curr_pos

    def rollback(self):
        """
        Rollback to last set mark position

        :raise: LexerError if no mark was set before
        """
        if self.mark_pos == self.NO_MARK:
            raise LexerError("Attempt to rollback with no mark")
        else:
            self.curr_pos = self.mark_pos

    def _skip_whitespaces(self):
        """
        Skip whitespaces from current pos to a first not-whitespace char
        """
        while True:
            symbol = self._get_next_symbol()
            if symbol == None:
                break
            elif not symbol.isspace():
                self._back()
                break

    def _get_next_symbol(self):
        try:
            symbol = self.input[self.curr_pos]
            self.curr_pos += 1
            return symbol
        except IndexError as ie:
            return None

    def _expect(self, expected):
        """
        Read one symbol from input string and check if it equals to expected

        :param expected: expected symbol
        :raise: LexerError if read symbol isn't equal to an expected one.

        """
        read = self._get_next_symbol()
        if read != expected:
            raise LexerError("Expected '" + expected + "' but read '" + read + "'")

    def _back(self):
        """
        Go one step backward in input string if possible
        """
        if self.curr_pos != 0:
            self.curr_pos -= 1

class ParseTreeElement:
    pass

class ParserElement:
    def parse(self, lexer):
        raise NotImplementedError()

class OR(ParserElement):
    def __init__(self, *parsers):
        self.parsers = parsers

    def parse(self, lexer):
        lexer.mark()

        for parser in self.parsers:
            result = parser.parse(lexer)

            if result != None:
                return result
            lexer.rollback()

        return None


class LexerError(Exception):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg

    def __str__(self):
        return "LexerError(" + self.msg + ")"


class ParserError(Exception):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg

    def __str__(self):
        return "ParserError(" + self.msg + ")"