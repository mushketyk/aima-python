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

token_type_names = {
    TokenTypes.EOL : "EOL",
    TokenTypes.BICONDITIONAL : "BICONDITIONAL",
    TokenTypes.IMPLICATION : "IMPLICATION",
    TokenTypes.NOT : "NOT",
    TokenTypes.OR : "OR",
    TokenTypes.AND : "AND",
    TokenTypes.LEFT_PAR : "LEFT_PAR",
    TokenTypes.RIGHT_PAR : "RIGHT PAR",
    TokenTypes.TRUE : "TRUE",
    TokenTypes.FALSE : "FALSE",
    TokenTypes.IDENTIFIER : "IDENTIFIER",
}

def get_token_type_name(token_type):
    return token_type_names[token_type]

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

class Term:
    def __init__(self, type, children):
        self.type = type
        self.children = list(children)

    def accept_visitor(self, visitor):
        raise NotImplementedError()

    def __eq__(self, other):
        if not isinstance(other, Term):
            return False

        if self.type != other.type:
            return False

        l1 = len(self.children)
        l2 = len(other.children)

        if l1 != l2:
            return False

        for i in range(l1):
            if self.children != other.children:
                return False

        return True

    def __hash__(self):
        return super().__hash__()

    def __str__(self):
        result = "(" + get_token_type_name(self.type)

        l = len(self.children)
        for i in range(l):
            result += str(self.children[i])

            if i != l - 1:
                result += ","

        result += ")"

        return result


class FunctionTerm(Term):
    def __init__(self, type, children):
        super().__init__(type, children)

    def accept_visitor(self, visitor):
        for child in self.children:
            child.accept_visitor(visitor)
            
        visitor.visit_function_term(self)

class NotTerm(FunctionTerm):
    def __init__(self, term):
        super().__init__(TokenTypes.NOT, [term])

class AndTerm(FunctionTerm):
    def __init__(self, left_term, right_term):
        super().__init__(TokenTypes.AND, [left_term, right_term])

class OrTerm(FunctionTerm):
    def __init__(self, left_term, right_term):
        super().__init__(TokenTypes.OR, [left_term, right_term])

class ImplicationTerm(FunctionTerm):
    def __init__(self, left_term, right_term):
        super().__init__(TokenTypes.IMPLICATION, [left_term, right_term])

class BiconditionalTerm(FunctionTerm):
    def __init__(self, left_term, right_term):
        super().__init__(TokenTypes.BICONDITIONAL, [left_term, right_term])

class TrueTerm(Term):
    def __init__(self):
        super().__init__(TokenTypes.TRUE, [])

    def accept_visitor(self, visitor):
        visitor.visit_true_term(self)

class FalseTerm(Term):
    def __init__(self):
        super().__init__(TokenTypes.FALSE, [])

    def accept_visitor(self, visitor):
        visitor.visit_false_term(self)

class SymbolTerm(Term):
    def __init__(self, name):
        super().__init__(TokenTypes.IDENTIFIER, [])
        self.name = name

    def accept_visitor(self, visitor):
        visitor.visit_symbol_term(self)

    def __eq__(self, other):
        if not isinstance(other, SymbolTerm):
            return False

        return self.name == other.name

    def __hash__(self):
        return super().__hash__()

    def __str__(self):
        return "(SymbolTerm " + self.name + ")"


class Parser:
    """
    Basic class for creating parsers
    """
    def parse(self, lexer):
        self.lexer = lexer
        return self._implementation_specific_parsing()

    def _implementation_specific_parsing(self):
        """
        Method that should be implemented to parse

        :return (Term): root term of the syntactics tree
        """
        raise NotImplementedError()

    def _match(self, token_type):
        """
        Check if next token is equal to the expected token type

        :param token_type: expected token type
        :raise: ParserError if unexpected token read
        """
        token = self._get_token()
        if token.type != token_type:
            raise ParserError("Unexpected token type")

    def _get_token(self):
        """
        Get next token from lexical analyser.

        :return: next token from lexical analyser
        """
        return self.lexer.get_next_token()



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


class TermVisitor:

    def visit_true_term(self, term):
        pass

    def visit_false_term(self, term):
        pass

    def visit_symbol_term(self, term):
        pass

    def visit_function_term(self, term):
        pass